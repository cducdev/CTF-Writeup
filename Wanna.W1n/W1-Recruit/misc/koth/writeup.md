# KOTH - Build a Snake Bot

| Competition | W1 Recruit |
| ----------- | ---------- |
| Category    | Misc       |

## Overview

> Challenge yêu cầu viết một bot chơi rắn trên bàn cờ `25 x 25`, có `12` quả táo và tối đa `1000` lượt. Mỗi lượt, hàm `decide(state)` trả về một trong ba hành động: đi thẳng (`0`), rẽ trái (`1`) hoặc rẽ phải (`2`). Hai bot chọn nước đi đồng thời, sau đó bàn cờ mới cập nhật.
>
> Ăn táo sẽ làm rắn dài thêm, còn đâm vào tường hoặc thân rắn thì chết. Nếu cả hai sống đến lượt `1000`, trận đấu sẽ so số táo tính điểm, độ dài, tổng số táo rồi đến số kill. Nếu cả hai chết cùng lúc, rắn dài hơn thắng; bằng nhau thì chơi lại với seed mới.

## Solution

Lúc đọc đề, mình thấy format của challenge khá giống các bài IOI dùng grader: mình chỉ cần cài đặt hàm `decide(state)`, còn hệ thống sẽ gọi hàm đó và xử lý phần còn lại. Vì có nền tảng lập trình thi đấu nên mình khá hứng thú với bài này, cảm giác có chút quen thuộc giữa một giải CTF :v

Quan sát tham lam của mình khá đơn giản: **rắn càng dài thì càng chiếm nhiều chỗ, khó xoay trở và càng dễ tự đâm vào thân**. Vì vậy, mình ưu tiên sống lâu nhất có thể và chờ đối thủ tự thua. Bot vẫn ăn táo khi có đường an toàn, nhưng việc kiếm táo được xếp sau việc tránh chết và giữ đường thoát.

Để triển khai ý tưởng này, mình dùng **BFS** để ước lượng vùng trống mà rắn có thể đi tới sau mỗi nước đi.

Để né việc chạm vào thân của chính mình, mình dùng thêm một ý tưởng tham lam là so sánh **số ô mà đầu rắn có thể đi tới với chiều dài thân**. Nếu số ô này ít hơn chiều dài thân thì rắn dễ bị kẹt và tự đâm vào mình. Vì vậy, mình ưu tiên hướng đi có đủ chỗ cho thân rắn; nếu hướng nào cũng thiếu chỗ thì chọn hướng thiếu ít nhất. Đây là ý nghĩa của `min(area - length, 0)` trong code bên dưới.

Đầu tiên, bot cần tự theo dõi vị trí hai con rắn. Ở lượt đầu, mình lấy thân rắn từ `initial_self_body` và `initial_opponent_body`, rồi suy ra hướng đi từ đầu và đốt thân liền sau. Các lượt tiếp theo, mình dùng hành động đã chọn cùng `last_opponent_action` để cập nhật hai thân rắn. Nếu đầu mới nằm trên một quả táo của lượt trước thì giữ đuôi để tăng độ dài, còn không thì bỏ đốt đuôi.

Sau đó, với từng hành động trong ba lựa chọn:

1. Loại nước đi đâm vào tường hoặc ô đang có thân rắn.
2. Đánh dấu các ô mà đầu đối thủ có thể tới trong lượt này để hạn chế va chạm trực diện.
3. Giả lập nước đi của mình, bỏ đuôi nếu không ăn táo, rồi chạy BFS từ đầu mới.
4. Đếm số ô đi tới được (`area`), số lối ra không bị chặn hay bị đầu đối thủ đe dọa (`exits`) và khoảng cách tới quả táo gần nhất (`food`).

Phần chọn nước đi trong [bfs_bot.cpp](./bfs_bot.cpp) dùng thứ tự ưu tiên sau:

```cpp
int length = int(body[0].size()) + grow;

array<int, 6> score = {
    !danger[head],
    exits > 0,
    min(area - length, 0),
    grow,
    -food,
    area
};

if (!found || score > best) {
    found = true;
    best = score;
    answer = a;
}
```

Bot ưu tiên tránh ô có nguy cơ đụng đầu đối thủ, còn lối thoát và ít thiếu không gian so với độ dài thân. Khi các tiêu chí này bằng nhau, bot mới ưu tiên ăn táo ngay, đi gần táo hơn, rồi chọn vùng rộng hơn.

Source đầy đủ để submit: [bfs_bot.cpp](./bfs_bot.cpp).
