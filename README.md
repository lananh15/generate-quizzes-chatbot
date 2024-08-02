## ⚠️ Requirements
    Python = 3.12.x

## :arrow_down: Installation

**1. Clone repository**

**2. Tải các thư viện cần thiết**
    ```bash
    pip install -r requirements.txt
    ```

**3. Chạy python server**
  - Nếu muốn dùng chatbot với dữ liệu được lưu trên pinecone (có raw-data và structured-data) thì xem file **pinecone-with-raw-data.md** và **pinecone-with-structured-data.md** hướng dẫn tương ứng trong các thư mục pinecone/raw-data và pinecone/structured-data.
  - Nếu muốn dùng chatbot với dữ liệu được lưu trên elasticsearch thì xem file **elasticsearch.md** hướng dẫn trong thư mục elasticsearch.

**Lưu ý:** Để dùng được chatbot sinh câu hỏi, bạn phải tạo file **config.json** trong thư mục gốc là **generate-quizzes-chatbot** với nội dung là các API key (của bạn) tương ứng như hình dưới đây:  

![config](https://github.com/user-attachments/assets/0281a81b-0cad-4667-afd1-dd5dd0e162c1)

## 📝 About Chatbot
Chatbot hỗ trợ sinh câu hỏi cho môn học "Quản lý dự án CNTT" với nội dung môn học gồm 8 chương:  
**1. Tổng quan**
- Khái niệm về quản lý
- Sự cần thiết của quản lý dự án
  - Các thống kê về quản lý dự án
  - Dự án thất bại
  - Ưu điểm của quản lý dự án
- Khái niệm dự án
  - Khái niệm
  - 4 yếu tố quan trọng
  - Các thuộc tính của dự án
  - Dự án công nghệ thông tin
- Phân loại dự án
  - Theo tầm cỡ dự án
  - Theo nội dung dự án
  - Các cách phân loại khác
- Quản lý dự án là gì
- Các giai đoạn của dự án Công nghệ Thông Tin
  - Giai đoạn xác định
  - Giai đoạn phân tích
  - Giai đoạn thiết kế
  - Giai đoạn thực hiện
  - Giai đoạn kiểm thử hệ thống
  - Giai đoạn kiểm thử chấp nhận
  - Giai đoạn vận hành
**2. Cơ cấu quản lý dự án**
- Bộ ba ràng buộc của quản lý dự án
- Các lĩnh vực kiến thức trong quản lý dự án
  - Chín lĩnh vực kiến thức cần phát triển
  - Bốn lĩnh vực quản lý cơ bản
  - Bốn lĩnh vực hỗ trợ
  - Lĩnh vực tích hợp (project integration management)
- Các công cụ và kỹ thuật
- Các kỹ năng cần thiết
**3. Quy trình quản lý dự án**
- Quy trình khởi động
- Quy trình lập kế hoạch
- Quy trình thực thi
- Quy trình điều khiển
- Quy trình kết thúc
**4. Quản lý phạm vi**
- Quản lý phạm vi là gì
- Khởi động (Initiation)
  - Quy trình chọn dự án
  - Phương pháp chọn lựa dự án
  - Project Charter (tuyên bố dự án)
- Lập kế hoạch phạm vi (Scope Planning)
- Xác định phạm vi (Scope Definition)
- Cấu trúc phân rã công việc (WBS – Work Break-down Structure)
- Kiểm tra và điều khiển thay đổi phạm vi (Verification & Controling)
**5. Quản lý thời gian**
- Giới thiệu
- Các quy trình quản lý thời gian dự án
  - Xác định các hoạt động
  - Sắp xếp thứ tự các hoạt động
  - Ước lượng thời gian cho mỗi hoạt động
  - Phát triển lịch biểu
  - Kiểm soát lịch biểu
- Các công cụ và kỹ thuật ước lượng thời gian
  - Sử dụng ý kiến chuyên gia
  - Ước lượng dựa vào lịch sử
  - Kỹ thuật PERT
  - Phương pháp đường găng CPM
  - Sơ đồ Gantt
- Các kỹ thuật rút ngắn lịch biểu
- Kết luận
**6. Quản lý chi phí**
- Giới thiệu
- Khái niệm về quản lý chi phí
- Quy trình quản lý chi phí
  - Lập kế hoạch quản lý chi phí
  - Ước lượng chi phí
  - Dự toán ngân sách
  - Kiểm soát – điều chỉnh
- Lập kế hoạch quản lý chi phí
- Ước lượng chi phí
  - Các loại ước lượng chi phí
  - Các phương pháp để ước lượng chi phí dự án
- Dự toán chi phí
- Kiểm soát và điều chỉnh chi phí
- EVM (Earned Value Management)
**7. Quản lý rủi ro**
- Khái niệm rủi ro
- Quy trình quản lý rủi ro
  - Xác định rủi ro
  - Phân tích rủi ro
  - Lập kế hoạch đối phó
  - Kiểm soát rủi ro
**8. Quản lý chất lượng**
- Khái niệm
- Quy trình quản lý chất lượng
  - Lập kế hoạch quản lý chất lượng
  - Thực hiện đảm bảo chất lượng
  - Kiểm soát chất lượng
- Các công cụ và kỹ thuật quản lý chất lượng
  - Seven Basic Tools
    - Biểu đồ nguyên nhân kết quả (xương cá)
    - Biểu đồ kiểm soát
    - Phiếu kiểm soát (checksheet)
    - Biểu đồ phân tán (scatter diagram)
    - Biểu đồ tần suất (histogram)
    - Biểu đồ Pareto
    - Biểu đồ flowchart
  - Six sigma
