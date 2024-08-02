# generate-quizz-chatbot

### ⚠️ Requirements
    Python = 3.12.x

## :arrow_down: Installation

1. Clone repository.

2. Tải các thư viện cần thiết
    ```bash
    pip install -r requirements.txt
    ```

3. Chạy python server
  - Nếu muốn dùng chatbot với dữ liệu được lưu trên pinecone (có raw-data và structured-data) thì xem file **pinecone-with-raw-data.md** và **pinecone-with-structured-data.md** hướng dẫn tương ứng trong các thư mục pinecone/raw-data và pinecone/structured-data.
  - Nếu muốn dùng chatbot với dữ liệu được lưu trên elasticsearch thì xem file **elasticsearch.md** hướng dẫn trong thư mục elasticsearch.

**Lưu ý:** Để dùng được chatbot sinh câu hỏi, bạn phải tạo file config.json trong thư mục gốc là generate-quizzes-chatbot với nội dung là các API key (của bạn) tương ứng như hình dưới đây:  

![config](https://github.com/user-attachments/assets/0281a81b-0cad-4667-afd1-dd5dd0e162c1)
