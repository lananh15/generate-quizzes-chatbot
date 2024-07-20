## Tải và sử dụng Elasticsearch với Docker Desktop

**1. Tải Elasticsearch**  
Mở Command Prompt:
  - Chạy lệnh: ```docker pull elasticsearch:8.14.3``` để tải Elasticsearch.
  - Kiểm tra đã tải thành công Elasticsearch hay chưa: ```docker images``` nếu thành công sẽ hiển thị "elasticsearch" ở cột REPOSITORY.

**2. Sử dụng Elasticsearch**  
Chạy elasticsearch container: ```docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security enabled=false" elasticsearch:8.14.3```. Kiểm tra bằng cách truy cập http://localhost:9200/ nếu đã chạy thành công thì web sẽ hiển thị thông tin chi tiết về cấu hình và phiên bản của cluster Elasticsearch.  

Về sau chỉ cần vào Docker Desktop -> Chọn tab Containers và Run elasticsearch container (không cần viết lệnh trên Command Prompt nữa).  

**Lưu ý:** Nếu đã tải Elasticsearch và chạy container nhưng không truy cập được http://localhost:9200/ thì tìm và mở file **elasticsearch.yml** trên máy, những chỗ nào có "true" thì đổi thành "false" rồi truy cập lại localhost. Mỗi lần chạy elasticsearch container cần phải chờ khởi động khoảng 30 giây sau đó truy cập vào localhost sẽ ổn định hơn.

## Tải và sử dụng Kibana với Docker Desktop (nếu cần)

**1. Tải Kibana**    
Mở Docker Desktop:
  - Tìm image Kibana trên Docker Desktop và Pull về máy.  

**2. Sử dụng Kibana**  
Mở Command Prompt:
  - Kiểm tra đã tải thành công Kibana hay chưa: ```docker images``` nếu thành công sẽ hiển thị "kibana" ở cột REPOSITORY.
  - Chạy Kibana container: ```docker run -d --name kibana --link elasticsearch:elasticsearch -p 5601:5601 kibana:8.14.3```. Kiểm tra bằng cách truy cập http://localhost:5601/ nếu đã chạy thành công thì web sẽ hiển thị giao diện của Kibana.
    
  **Lưu ý:** Phải Run elasticsearch container trước và Run kibana container sau thì Kibana sẽ kết nối được với Elasticsearch.  

Bật tab Dev Tools trên giao diện của Kibana và có thể thử 1 số lệnh cơ bản sau đây:
  - **Xem tất cả index trên Elasticsearch:** ```GET /_cat/indices?v```
  - **Tạo index mới:** ```PUT /indexname1?pretty``` trong đó [indexname1] là tên của index bạn muốn tạo.
  - **Xoá index bất kì:** ```DELETE /indexname1``` trong đó [indexname1] là tên của index bạn muốn xoá.
  - **Xem mapping của index bất kì:** ```GET /indexname1/_mapping``` trong đó [indexname1] là tên của index bạn muốn xem mapping.  

  **Lưu ý:** Bạn cũng có thể dùng code Python để thực hiện các chức năng trên nếu không muốn sử dụng Kibana.  

## :computer: Dùng chatbot hỗ trợ sinh câu hỏi (sử dụng elasticsearch)
**1. Lưu cấu trúc dữ liệu từ file .json lên Elasticsearch**  
  - Khởi động elasticsearch container.
  - Run file **index_to_elasticsearch.py** để có thể lưu dữ liệu từ file **qtda.json** lên Elasticsearch, chatbot sẽ sử dụng dữ liệu trên Elasticsearch để tạo câu hỏi cho môn học.  

**2. Sử dụng chatbot**  
  - Run file **app.py** và truy cập vào http://127.0.0.1:5000/ để dùng chatbot ở localhost.
  - Các cú pháp để dùng chatbot:  
    - **Xem cấu trúc chương, tiêu đề chính, tiêu đề phụ, tiểu mục của môn học mà chúng tôi hỗ trợ:** ```chương hỗ trợ```
    - **Tạo số lượng câu hỏi cho chương bất kì:** ```chapter: [tên chương]: [số lượng câu hỏi (tối đa 25)]```  
    - **Tạo số lượng câu hỏi cho tiêu đề chính bất kì:** ```heading: [tên tiêu đề chính]: [số lượng câu hỏi (tối đa 15)]```  
    - **Tạo số lượng câu hỏi cho tiêu đề phụ bất kì:** ```subheading: [tên tiêu đề phụ]: [số lượng câu hỏi (tối đa 10)]```  
    - **Tạo số lượng câu hỏi cho tiểu mục bất kì:** ```subsubheading: [tên tiểu mục]: [số lượng câu hỏi (tối đa 5)]```





