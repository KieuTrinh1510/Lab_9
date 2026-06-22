# BÀI THỰC HÀNH KIỂM THỬ TỰ ĐỘNG VỚI SELENIUM

## 1. Thông tin sinh viên

| Thông tin | Nội dung |
|---|---|
| Họ và tên | **Nguyễn Thị Kiều Trinh** |
| Mã sinh viên | **23010632** |


## 2. Giới thiệu

Project sử dụng **Selenium WebDriver** kết hợp với **pytest** để kiểm thử tự động các chức năng chính của website [SauceDemo](https://www.saucedemo.com/).

SauceDemo là website thương mại điện tử dùng cho mục đích thực hành kiểm thử. Project thực hiện **12 test case**, nhiều hơn yêu cầu tối thiểu 03 test case của bài tập.

Mục tiêu:

- Làm quen với Selenium WebDriver và cách định vị phần tử HTML.
- Tự động hóa các thao tác của người dùng trên trình duyệt.
- Sử dụng assertion để so sánh kết quả thực tế với kết quả mong đợi.
- Tổ chức và chạy test tự động bằng pytest.
- Sử dụng fixture để khởi tạo và đóng trình duyệt sau mỗi test.

## 3. Tài liệu tự học

- [Selenium WebDriver - Getting started](https://www.selenium.dev/documentation/webdriver/getting_started/)
- [Selenium - Write your first script](https://www.selenium.dev/documentation/webdriver/getting_started/first_script/)
- [pytest - Get started](https://docs.pytest.org/en/stable/getting-started.html)
- [webdriver-manager trên PyPI](https://pypi.org/project/webdriver-manager/)

## 4. Công nghệ sử dụng

| Công nghệ | Mục đích |
|---|---|
| Python | Ngôn ngữ lập trình test |
| Selenium WebDriver | Điều khiển và tự động hóa trình duyệt |
| pytest | Tổ chức, thực thi và báo cáo test |
| webdriver-manager | Tự động tải và quản lý ChromeDriver |
| Google Chrome | Trình duyệt thực thi kiểm thử |

Các test được cấu hình chạy ở chế độ **headless**, vì vậy không cần mở cửa sổ Chrome khi chạy.

## 5. Cấu trúc project

```text
lab9/
├── tests/
│   ├── test_login.py
│   ├── test_product.py
│   └── test_cart_checkout.py
├── .gitignore
├── requirements.txt
└── README.md
```

## 6. Danh sách test case

### Nhóm 1: Kiểm thử đăng nhập

| Mã | Kịch bản | Kết quả mong đợi |
|---|---|---|
| TC-01 | Đăng nhập bằng tài khoản hợp lệ | Chuyển đến trang Products |
| TC-02 | Đăng nhập với mật khẩu sai | Hiển thị thông báo username/password không đúng |
| TC-03 | Đăng nhập bằng tài khoản bị khóa | Hiển thị thông báo tài khoản đã bị khóa |
| TC-04 | Đăng nhập khi để trống username | Hiển thị thông báo Username is required |

### Nhóm 2: Kiểm thử sản phẩm

| Mã | Kịch bản | Kết quả mong đợi |
|---|---|---|
| TC-05 | Kiểm tra danh sách sản phẩm | Hiển thị đủ 6 sản phẩm |
| TC-06 | Sắp xếp theo giá từ thấp đến cao | Giá sản phẩm được sắp xếp tăng dần |
| TC-07 | Sắp xếp tên sản phẩm từ Z đến A | Tên sản phẩm được sắp xếp đúng thứ tự |
| TC-08 | Mở trang chi tiết sản phẩm | Tên sản phẩm ở trang chi tiết chính xác |

### Nhóm 3: Kiểm thử giỏ hàng và thanh toán

| Mã | Kịch bản | Kết quả mong đợi |
|---|---|---|
| TC-09 | Thêm một sản phẩm vào giỏ hàng | Badge hiển thị 1 và sản phẩm xuất hiện trong giỏ |
| TC-10 | Xóa sản phẩm khỏi giỏ hàng | Giỏ hàng trống và badge biến mất |
| TC-11 | Hoàn tất quy trình checkout | Hiển thị thông báo Thank you |
| TC-12 | Checkout khi thiếu First Name | Hiển thị thông báo First Name is required |

## 7. Dữ liệu kiểm thử

Website cung cấp sẵn tài khoản thực hành:

| Loại tài khoản | Username | Password |
|---|---|---|
| Tài khoản hợp lệ | `standard_user` | `secret_sauce` |
| Tài khoản bị khóa | `locked_out_user` | `secret_sauce` |

Dữ liệu checkout:

| Trường | Giá trị |
|---|---|
| First Name | `Nguyen` |
| Last Name | `Van A` |
| Postal Code | `700000` |

## 8. Kết quả thực hiện

Kết quả mong đợi khi chạy toàn bộ project:

```text
============================= test session starts =============================
collected 12 items

tests/test_login.py ....                                      [ 33%]
tests/test_product.py ....                                    [ 66%]
tests/test_cart_checkout.py ....                              [100%]

============================= 12 passed ==============================
```

> Lưu ý: Thời gian chạy phụ thuộc vào tốc độ mạng, phiên bản Chrome và quá trình tải ChromeDriver ở lần chạy đầu tiên.

## 9. Kiến thức đạt được

Sau bài thực hành, sinh viên đã áp dụng được:

- Khởi tạo và cấu hình Chrome WebDriver.
- Tìm phần tử bằng `ID`, `CLASS_NAME` và `CSS_SELECTOR`.
- Thực hiện các thao tác nhập liệu, click và chọn giá trị trong dropdown.
- Sử dụng implicit wait và explicit wait.
- Kiểm tra nội dung, URL, số lượng phần tử và trạng thái hiển thị.
- Viết test case tích cực và tiêu cực.
- Quản lý vòng đời trình duyệt bằng pytest fixture.
- Chạy nhiều test case và đọc báo cáo kết quả từ pytest.

## 10. Kết luận

Project đã xây dựng thành công 12 test case Selenium cho các chức năng đăng nhập, xem và sắp xếp sản phẩm, quản lý giỏ hàng và checkout trên SauceDemo. Các test giúp giảm thao tác kiểm thử thủ công, có thể chạy lại nhiều lần và phát hiện nhanh khi chức năng của website không còn hoạt động đúng như mong đợi.
