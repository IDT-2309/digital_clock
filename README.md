### Hướng dẫn cài đặt 
1. Clone repository
```bash 
 git clone https://github.com/IDT-2309/digital_clock
```

2. Install dependencies
```bash 
cd digital_clock
pip install -r requirements.txt
```
3. Run project 
```bash 
python3 digital_clock.py
```
### I. Lưu đồ thuật toán

### II. Module sử dụng

### Phân tích chi tiết Module `mixer`

#### 1. **Khởi tạo (`init`):**

- **Chức năng:**
  - Khởi tạo hệ thống mixer để chuẩn bị cho các thao tác âm thanh như phát nhạc, điều khiển âm lượng, và các hiệu ứng âm thanh khác.

- **Hình thức:**
  - Được thực hiện bằng cách gọi hàm `mixer.init()`.

- **Cách thức:**
  - `mixer.init()` là một lệnh đơn giản, không cần tham số đầu vào và không trả về giá trị.

- **Kết quả:**
  - Hệ thống mixer được khởi tạo, sẵn sàng để thực hiện các thao tác âm thanh tiếp theo.

```python
mixer.init()
```

#### 2. **Dừng nhạc (`music_stop`):**

- **Chức năng:**
  - Dừng phát nhạc ngay lập tức.

- **Hình thức:**
  - Được thực hiện bằng cách gọi hàm `music_stop()`.

- **Cách thức:**
  - Trong hàm `music_stop()`, gọi `mixer.music.fadeout(0)` để dừng nhạc. Tham số `0` nghĩa là dừng ngay lập tức mà không có hiệu ứng fade out.

- **Kết quả:**
  - Nhạc sẽ dừng ngay lập tức.

```python
def music_stop():
    mixer.music.fadeout(0)
```

#### 3. **Cập nhật âm lượng (`volume_slider_update`):**

- **Chức năng:**
  - Cập nhật âm lượng của nhạc dựa trên giá trị của slider.

- **Hình thức:**
  - Được thực hiện bằng cách gọi hàm `volume_slider_update(music_volume_param)` với tham số đầu vào là giá trị âm lượng hiện tại.

- **Cách thức:**
  - Lấy giá trị mới từ slider: `volume_slider_value = volume_slider.get() / 10`.
  - Kiểm tra nếu giá trị mới khác với giá trị hiện tại: `if volume_slider_value != music_volume_param:`.
  - Cập nhật âm lượng: `mixer.music.set_volume(volume_slider_value)`.
  - Cập nhật giá trị âm lượng hiện tại: `music_volume_param = volume_slider_value`.

- **Kết quả:**
  - Âm lượng của nhạc sẽ thay đổi tương ứng với vị trí của slider.

```python
def volume_slider_update(music_volume_param):
    # Lấy giá trị mới nhất từ slider
    volume_slider_value = volume_slider.get() / 10
    
    # Cập nhật âm lượng nếu có sự thay đổi vị trí/giá trị của slider
    if volume_slider_value != music_volume_param:
        mixer.music.set_volume(volume_slider_value)
        music_volume_param = volume_slider_value
        music.volume = volume_slider_value
```

#### 4. **Tải và phát nhạc (`music_load_play`):**

- **Chức năng:**
  - Tải một file nhạc và bắt đầu phát nhạc.

- **Hình thức:**
  - Được thực hiện bằng cách gọi hàm `music_load_play()`.

- **Cách thức:**
  - Tải file nhạc: `mixer.music.load(Path(working_directory, 'themes', theme_selected, 'music.mp3'))`.
  - Đặt âm lượng: `mixer.music.set_volume(music.volume)`.
  - Bắt đầu phát nhạc: `mixer.music.play(loops=-1)` với tham số `loops=-1` để lặp lại vô hạn.

- **Kết quả:**
  - Nhạc sẽ được tải và phát với âm lượng đã cài đặt trước.

```python
def music_load_play():
    mixer.music.load(Path(working_directory, 'themes', theme_selected, 'music.mp3'))
    mixer.music.set_volume(music.volume)
    mixer.music.play(loops=-1)
```

### Kết quả tổng quan của các module
- Các module này cho phép quản lý hệ thống âm thanh từ khởi tạo, dừng nhạc, điều chỉnh âm lượng, đến việc tải và phát nhạc. Chúng cung cấp một cách thức linh hoạt để điều khiển và quản lý âm thanh trong ứng dụng.

![](/docs/mixer.png)

### Phân tích chi tiết Module `Converter` và `Solar`

#### 1. **Lấy ngày hiện tại và tách thành các phần tử:**

- **Chức năng:**
  - Lấy ngày hiện tại theo định dạng dương lịch và tách ngày thành các phần tử ngày, tháng, năm.

- **Hình thức:**
  - Sử dụng hàm `strftime` để lấy ngày hiện tại và hàm `split` để tách chuỗi ngày tháng năm.

- **Cách thức:**
  - `solar = strftime('%d-%m-%Y')`: Lấy ngày hiện tại với định dạng `ngày-tháng-năm`.
  - `solar = solar.split('-')`: Tách chuỗi ngày thành danh sách các phần tử.

- **Kết quả:**
  - Chuỗi ngày hiện tại được tách thành danh sách các phần tử `ngày`, `tháng`, `năm`.

```python
from time import strftime

# Lấy ngày hiện tại và tách thành các phần tử
solar = strftime('%d-%m-%Y')
solar = solar.split('-')
```

#### 2. **Tạo đối tượng `Solar`:**

- **Chức năng:**
  - Tạo đối tượng `Solar` từ danh sách các phần tử ngày, tháng, năm.

- **Hình thức:**
  - Sử dụng hàm `Solar` để tạo đối tượng.

- **Cách thức:**
  - `solar = Solar(int(solar[2]), int(solar[1]), int(solar[0]))`: Chuyển đổi các phần tử năm, tháng, ngày sang kiểu số nguyên và tạo đối tượng `Solar`.

- **Kết quả:**
  - Đối tượng `Solar` được tạo ra từ ngày hiện tại.

```python
from lunarcalendar import Solar

# Tạo đối tượng Solar
solar = Solar(int(solar[2]), int(solar[1]), int(solar[0]))
```

#### 3. **Chuyển đổi ngày dương lịch sang ngày âm lịch (`Solar2Lunar`):**

- **Chức năng:**
  - Chuyển đổi ngày tháng dương lịch (Gregorian) sang ngày tháng âm lịch (Lunar).

- **Hình thức:**
  - Sử dụng hàm `Converter.Solar2Lunar` để thực hiện chuyển đổi.

- **Cách thức:**
  - `lunar_date = Converter.Solar2Lunar(solar)`: Chuyển đổi đối tượng `Solar` sang ngày âm lịch.

- **Kết quả:**
  - Trả về đối tượng ngày âm lịch tương ứng.

```python
from lunarcalendar import Converter

# Chuyển đổi ngày dương lịch sang ngày âm lịch
lunar_date = Converter.Solar2Lunar(solar)
```

### Kết quả tổng quan của các module
- Các module này cho phép lấy ngày hiện tại theo lịch dương và chuyển đổi sang ngày âm lịch. Chúng cung cấp cách thức đơn giản và hiệu quả để làm việc với ngày tháng trong các ứng dụng yêu cầu xử lý lịch âm và lịch dương.

![](/docs/lunar.png)

### Phân tích chi tiết Module `PIL.Image` và `PIL.ImageTk`

#### 1. **Tạo ảnh (`image_generate`):**

- **Chức năng:**
  - Tạo và thay đổi kích thước ảnh từ một file ảnh có sẵn.

- **Hình thức:**
  - Sử dụng các hàm của thư viện `PIL` (Python Imaging Library) để mở, thay đổi kích thước và tạo đối tượng ảnh để sử dụng trong giao diện đồ họa.

- **Cách thức:**
  - `my_img_path = Path(working_directory, 'themes', 'img', picture_name)`: Xác định đường dẫn đến file ảnh.
  - `my_img = Image.open(my_img_path)`: Mở file ảnh.
  - `width = int(image_size)` và `height = int(image_size)`: Xác định kích thước mới cho ảnh.
  - `resized_image = my_img.resize((width, height))`: Thay đổi kích thước ảnh.
  - `photo = ImageTk.PhotoImage(resized_image)`: Tạo đối tượng ảnh để sử dụng trong giao diện Tkinter.

- **Kết quả:**
  - Trả về đối tượng ảnh đã thay đổi kích thước, sẵn sàng để sử dụng trong giao diện đồ họa.

```python
from PIL import Image
from PIL import ImageTk
from pathlib import Path

def image_generate(image_size, picture_name):
    my_img_path = Path(working_directory, 'themes', 'img', picture_name)
    my_img = Image.open(my_img_path)
    width = int(image_size)
    height = int(image_size)
    resized_image = my_img.resize((width, height))
    photo = ImageTk.PhotoImage(resized_image)
    return photo
```

#### 2. **Tạo chuỗi ảnh động (`img_seq_creation`):**

- **Chức năng:**
  - Tạo chuỗi ảnh từ file GIF và thay đổi kích thước các khung hình trong GIF.

- **Hình thức:**
  - Sử dụng các hàm của thư viện `PIL` để mở file GIF, lấy từng khung hình, thay đổi kích thước và chuyển đổi các khung hình thành đối tượng ảnh để sử dụng trong giao diện đồ họa.

- **Cách thức:**
  - `path_gif = Path(working_directory, 'themes', theme_selected, 'GIF.GIF')`: Xác định đường dẫn đến file GIF.
  - `gif_image = Image.open(path_gif)`: Mở file GIF.
  - `frames_count_all = gif_image.n_frames`: Lấy số lượng khung hình trong GIF.
  - `images_list = []`: Tạo danh sách rỗng để lưu các khung hình đã thay đổi kích thước.
  - Vòng lặp `for i in range(frames_count_all):` để xử lý từng khung hình:
    - `gif_image.seek(i)`: Đến khung hình thứ `i`.
    - `frame = gif_image.copy()`: Sao chép khung hình.
    - `scaled_frame = frame.resize((int(frame.width * scale_factor), int(frame.height * scale_factor)), Image.Resampling.LANCZOS)`: Thay đổi kích thước khung hình.
    - `images_list.append(ImageTk.PhotoImage(scaled_frame))`: Chuyển đổi khung hình thành đối tượng ảnh và thêm vào danh sách.
  - `return images_list, frames_count_all`: Trả về danh sách các khung hình đã thay đổi kích thước và số lượng khung hình.

- **Kết quả:**
  - Trả về danh sách các đối tượng ảnh từ các khung hình của GIF đã được thay đổi kích thước, sẵn sàng để sử dụng trong giao diện đồ họa.

```python
from PIL import Image
from PIL import ImageTk
from pathlib import Path

def img_seq_creation(scale_factor):
    path_gif = Path(working_directory, 'themes', theme_selected, 'GIF.GIF')
    gif_image = Image.open(path_gif)
    frames_count_all = gif_image.n_frames
    images_list = []

    for i in range(frames_count_all):
        # Load từng khung hình
        gif_image.seek(i)
        frame = gif_image.copy()
        # Thay đổi kích thước khung hình
        scaled_frame = frame.resize((int(frame.width * scale_factor), int(frame.height * scale_factor)), Image.Resampling.LANCZOS)
        # Chuyển đổi khung hình thành đối tượng ảnh và thêm vào danh sách
        images_list.append(ImageTk.PhotoImage(scaled_frame))

    return images_list, frames_count_all
```

### Kết quả tổng quan của các module
- Các module này cho phép xử lý ảnh và ảnh động (GIF) từ file, bao gồm việc mở, thay đổi kích thước và chuyển đổi các khung hình thành đối tượng ảnh để sử dụng trong giao diện đồ họa Tkinter. Điều này giúp việc quản lý và hiển thị ảnh trong ứng dụng trở nên linh hoạt và dễ dàng hơn.

![](/docs/animation.png)

### III. Demo



### Phụ lục
- Cấu trúc thư mục:
.
├── README.md
├── digital_clock.py                      : mã nguồn chính
├── docs                                  : chứa các tài liệu ảnh trong md
│   ├── animation.png                 
│   ├── diagram_alg.excalidraw.png
│   ├── lunar.png
│   ├── mixer.png
│   └── use_case.excalidraw.png
├── requirements.txt                       : các thư viện cần được cài đặt để có thể chạy
├── settings_db_tkinter.json               : file chứa cấu hình các phần hiển thị của thành phần trong digital_clock.py
└── themes                                 : thư mục lưu trữ ảnh, nhạc, icon. Gồm 2 chủ đề i_love_you và love
    ├── i_love_you                         : chủ đề
    │   ├── GIF.gif
    │   ├── icon.png
    │   └── music.mp3
    ├── img                                : chứa ảnh về các thành phần trong chức năng settings
    │   ├── animation_speed.png
    │   ├── close.png
    │   ├── settings.png
    │   ├── start.png
    │   ├── stop.png
    │   ├── theme_switch.png
    │   └── volume.png
    └── love                                : chủ đề
        ├── GIF.gif
        ├── icon.png
        └── music.mp3


- chú thích về file settings_db_tkinter.json
### Tài liệu về Cấu trúc Dictionary trong Cấu hình Giao diện

Dưới đây là mô tả chi tiết về cấu trúc và tác dụng của các dictionary trong cấu hình giao diện. Các dictionary này được sử dụng để tùy chỉnh giao diện người dùng cho từng chủ đề (theme) trong ứng dụng.

#### Dictionary chính:

- **theme_selected**: Chứa tên của chủ đề hiện tại được chọn.
  - **Giá trị:** Chuỗi ký tự, ví dụ: `"i_love_you"`
  - **Tác dụng:** Xác định chủ đề hiện tại được sử dụng cho giao diện.

- **music_on**: Biến trạng thái bật/tắt nhạc.
  - **Giá trị:** Boolean, ví dụ: `false`
  - **Tác dụng:** Xác định liệu nhạc nền có đang được bật hay không.

- **themes**: Chứa các chủ đề khác nhau, mỗi chủ đề là một dictionary con.
  - **Giá trị:** Dictionary chứa các chủ đề con.
  - **Tác dụng:** Tùy chỉnh giao diện dựa trên từng chủ đề.

#### Dictionary con (ví dụ: `i_love_you`, `love`):

Mỗi chủ đề chứa các thuộc tính tùy chỉnh giao diện như sau:

1. **title**: Tiêu đề của chủ đề.
   - **Giá trị:** Chuỗi ký tự, ví dụ: `"i love you"`
   - **Tác dụng:** Đặt tiêu đề cho chủ đề.

2. **button_bg_color**: Màu nền của nút.
   - **Giá trị:** Chuỗi màu HEX, ví dụ: `"#675C7C"`
   - **Tác dụng:** Xác định màu nền của nút trong giao diện.

3. **button_bg_color_clicked**: Màu nền của nút khi được nhấn.
   - **Giá trị:** Chuỗi màu HEX, ví dụ: `"#F5D2A5"`
   - **Tác dụng:** Xác định màu nền của nút khi được nhấn.

4. **button_pos_x**: Vị trí x của nút.
   - **Giá trị:** Số nguyên, ví dụ: `672`
   - **Tác dụng:** Xác định vị trí ngang (x) của nút trên giao diện.

5. **button_pos_y**: Vị trí y của nút.
   - **Giá trị:** Số nguyên, ví dụ: `24`
   - **Tác dụng:** Xác định vị trí dọc (y) của nút trên giao diện.

6. **time_font_color**: Màu chữ của thời gian.
   - **Giá trị:** Chuỗi màu HEX, ví dụ: `"#675C7C"`
   - **Tác dụng:** Xác định màu chữ hiển thị thời gian.

7. **time_font_style**: Kiểu chữ của thời gian.
   - **Giá trị:** Chuỗi ký tự, ví dụ: `"Forte"`
   - **Tác dụng:** Xác định kiểu chữ hiển thị thời gian.

8. **hour_minute_font_size**: Kích thước chữ của giờ và phút.
   - **Giá trị:** Số nguyên, ví dụ: `70`
   - **Tác dụng:** Xác định kích thước chữ cho giờ và phút.

9. **second_font_size**: Kích thước chữ của giây.
   - **Giá trị:** Số nguyên, ví dụ: `40`
   - **Tác dụng:** Xác định kích thước chữ cho giây.

10. **hour_minute_pos_x**: Vị trí x của giờ và phút.
    - **Giá trị:** Số nguyên, ví dụ: `380`
    - **Tác dụng:** Xác định vị trí ngang (x) của giờ và phút trên giao diện.

11. **hour_minute_pos_y**: Vị trí y của giờ và phút.
    - **Giá trị:** Số nguyên, ví dụ: `400`
    - **Tác dụng:** Xác định vị trí dọc (y) của giờ và phút trên giao diện.

12. **second_pos_x**: Vị trí x của giây.
    - **Giá trị:** Số nguyên, ví dụ: `380`
    - **Tác dụng:** Xác định vị trí ngang (x) của giây trên giao diện.

13. **second_pos_y**: Vị trí y của giây.
    - **Giá trị:** Số nguyên, ví dụ: `390`
    - **Tác dụng:** Xác định vị trí dọc (y) của giây trên giao diện.

14. **music_volume**: Âm lượng của nhạc nền.
    - **Giá trị:** Số thập phân từ 0.0 đến 1.0, ví dụ: `0.6`
    - **Tác dụng:** Xác định âm lượng của nhạc nền.

15. **date_font_color**: Màu chữ của ngày tháng.
    - **Giá trị:** Chuỗi màu HEX, ví dụ: `"#675C7C"`
    - **Tác dụng:** Xác định màu chữ hiển thị ngày tháng.

16. **date_font_style**: Kiểu chữ của ngày tháng.
    - **Giá trị:** Chuỗi ký tự, ví dụ: `"Forte"`
    - **Tác dụng:** Xác định kiểu chữ hiển thị ngày tháng.

17. **date_font_size**: Kích thước chữ của ngày tháng.
    - **Giá trị:** Số nguyên, ví dụ: `28`
    - **Tác dụng:** Xác định kích thước chữ cho ngày tháng.

18. **date_pos_x**: Vị trí x của ngày tháng.
    - **Giá trị:** Số nguyên, ví dụ: `50`
    - **Tác dụng:** Xác định vị trí ngang (x) của ngày tháng trên giao diện.

19. **date_pos_y**: Vị trí y của ngày tháng.
    - **Giá trị:** Số nguyên, ví dụ: `10`
    - **Tác dụng:** Xác định vị trí dọc (y) của ngày tháng trên giao diện.

20. **animation_speed**: Tốc độ của các hoạt ảnh.
    - **Giá trị:** Số nguyên, ví dụ: `10`
    - **Tác dụng:** Xác định tốc độ của các hoạt ảnh trong giao diện.

21. **canvas_settings_orentation**: Hướng của canvas.
    - **Giá trị:** Chuỗi ký tự, ví dụ: `"ne"`
    - **Tác dụng:** Xác định hướng của canvas trong giao diện.

22. **canvas_settings_pos_x_diff**: Sự khác biệt vị trí x của canvas.
    - **Giá trị:** Số nguyên, ví dụ: `-10`
    - **Tác dụng:** Xác định sự khác biệt về vị trí ngang (x) của canvas so với vị trí gốc.

23. **window_title**: Tiêu đề của cửa sổ.
    - **Giá trị:** Chuỗi ký tự, ví dụ: `"Thinking about how I Didn’t expect To fall in love Like this"`
    - **Tác dụng:** Xác định tiêu đề của cửa sổ ứng dụng.

