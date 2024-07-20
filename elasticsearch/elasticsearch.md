## Tải và sử dụng Elasticsearch với Docker Desktop

**1. Tải Elasticsearch**
Mở Command Prompt:
  - Chạy lệnh: ```docker pull elasticsearch:8.14.3``` để tải Elasticsearch.
  - Kiểm tra đã tải thành công Elasticsearch hay chưa: ```docker images``` nếu thành công sẽ hiển thị "elasticsearch" ở cột REPOSITORY.

**2. Sử dụng Elasticsearch**
Chạy elasticsearch container: ```docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security enabled=false" elasticsearch:8.14.3```. Kiểm tra bằng cách truy cập http://localhost:9200/ nếu đã chạy thành công thì web sẽ hiển thị thông tin chi tiết về cấu hình và phiên bản của cluster Elasticsearch.  

Về sau chỉ cần vào Docker Desktop -> Chọn tab Containers và Run elasticsearch container (không cần viết lệnh trên Command Prompt nữa).  

**Lưu ý:** Nếu đã tải Elasticsearch và chạy container nhưng không truy cập được http://localhost:9200/ thì tìm file **elasticsearch.yml** trên máy rồi những chỗ nào có "true" thì đổi thành "false" rồi truy cập lại localhost. Mỗi lần chạy elasticsearch container cần phải chờ khởi động khoảng 30 giây rồi truy cập vào localhost sẽ ổn định hơn.

## Tải và sử dụng Kibana với Docker Desktop

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



