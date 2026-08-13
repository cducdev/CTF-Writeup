# Jinja2 SSTI Lab

Lab Flask nhỏ để quan sát sự khác nhau giữa việc dùng input làm **mã template**
(cố ý vulnerable) và truyền input vào template như **dữ liệu** (safe).

> [!WARNING]
> App cố ý chứa SSTI. Chỉ chạy cục bộ trên `127.0.0.1`; không deploy và
> không mở port ra LAN/Internet.

## Chạy app

Yêu cầu Python 3.10+.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 app.py
```

Mở <http://127.0.0.1:8000>, nhập payload vô hại:

```jinja2
{{ 7 * 7 }}
```

- **Render vulnerable** trả về `49` vì input được Jinja biên dịch.
- **Render safe** trả về nguyên văn `{{ 7 * 7 }}` vì input chỉ là dữ liệu.

## Chạy test

```bash
python3 -m pytest -q
```

## Điểm cần quan sát

Lỗi nằm ở nhánh sau trong `app.py`:

```python
render_template_string(payload)
```

Cách đối chiếu an toàn giữ source template cố định và truyền input qua biến:

```python
render_template("index.html", result=payload)
```

Input được giới hạn 200 ký tự, app bind localhost, kết quả được escape khi đưa
vào trang ngoài, và response có các security header cơ bản. Những giới hạn này
chỉ giảm rủi ro cho lab; chúng **không biến nhánh vulnerable thành an toàn**.

Port `8000` được dùng thay cho `5000` vì macOS AirPlay Receiver thường dùng
port `5000` qua process `ControlCenter`, có thể khiến trình duyệt nhận HTTP 403.

## Cấu trúc

```text
app.py                 Flask app và hai cách render
templates/index.html   Giao diện lab
static/styles.css      Giao diện responsive
tests/test_app.py      Test route, SSTI, safe mode và headers
```
