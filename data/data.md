## Giải thích các file dữ liệu
**1. Trong thư mục rouge**  
  Trong thư mục pinecone-with-raw-data (chỉ để đo Rouge cho 1 pipeline dùng pinecone đã được lưu dữ liệu thô):  
  - Các file .txt trong thư mục **quizzes_txt** là các câu hỏi được tổng hợp thông qua chế độ ChatGPT, Gemini và Claude (bao gồm 410 câu hỏi được sinh ra từ tổng cộng 8 chương bài học).
  - Các file .json trong thư mục **quizzes_json** được lưu từ các file .txt trong thư mục **quizzes_txt** theo dạng có cấu trúc được dùng để đo độ Rouge.    

**2. Các file cùng cấp với thư mục rouge**  
  - File **qtda_raw.txt** là file tổng hợp các nội dung lý thuyết của 8 chương học, được lưu dưới dạng không cấu trúc và chia thành các đoạn văn bản phù hợp cách nhau bởi 1 dòng trống. Được dùng để lưu dữ liệu không cấu trúc lên pinecone (sử dụng trong thư mục cùng cấp với **data** là **pinecone-with-raw-data**)  
  - File **qtda.json** cũng giống như file **qtda_raw.txt** nhưng lại được tổ chức dưới dạng có cấu trúc. Được dùng để lưu dữ liệu có cấu trúc lên pinecone và elasticsearch (sử dụng trong thư mục cùng cấp với **data** là **pinecone-with-structured-data** và **elasticsearch**)