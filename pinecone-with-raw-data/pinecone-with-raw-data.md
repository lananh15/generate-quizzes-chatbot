
## :computer: Dùng chatbot hỗ trợ sinh câu hỏi (sử dụng Pinecone với dữ liệu thô)
**1. Lưu dữ liệu thô từ file qtda_raw.txt lên Pinecone (nếu muốn dùng index của riêng bạn trên pinecone, nếu không hãy xem mục số 2)**  
  - Run file **save_raw_data_to_pinecone.py** để có thể lưu dữ liệu từ file **qqtda_raw.txt** trong thư mục **data** lên Pinecone theo các vector, chatbot sẽ sử dụng dữ liệu trên Pinecone để tạo câu hỏi cho môn học.  

  **Lưu ý:** Thay đổi API key, tên index khác từ tài khoản Pinecone và có thể sử dụng openai_api_key của riêng bạn.  
  - Để làm được, bạn cần phải có tài khoản trên https://www.pinecone.io/ và tạo index. Sau đó thay đổi các giá trị **api_key**, **index_name**, **dimension** (nếu dùng mô hình text-embedding-ada-002 của openAI thì giữ nguyên 1536), **cloud** và **region** trong đoạn code dưới đây của file **save_structured_data_to_pinecone.py** sao cho phù hợp.
  ```python
    # Tạo đối tượng Pinecone
    pc = Pinecone(api_key="020a8257-5dd3-41f3-a710-53d7c6fac5d9")

    # Kết nối đến index đã tồn tại hoặc tạo mới nếu chưa tồn tại
    index_name = "generate-quizz"
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=1536,  # Đảm bảo dimension khớp với model embedding bạn sử dụng
            metric='euclidean',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        ) 
  ```  

  - Ngoài ra, cũng cần thay đổi **api_key** và **index** trong đoạn code dưới đây của file **app.py**  
  ```python
    if __name__ == '__main__':
    openai_handler = PineconeOpenAIHandler("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")
    pc = Pinecone(api_key="020a8257-5dd3-41f3-a710-53d7c6fac5d9")
    index = pc.Index("generate-quizz")
    app = PineconeQuizzSearchApp(openai_handler, index)
    app.run()
  ```  

**2. Sử dụng chatbot**  
  - Run file **app.py** và truy cập vào http://127.0.0.1:5000/ để dùng chatbot ở localhost.
  - Các cú pháp để dùng chatbot:  
    - **Xem các chương mà chatbot hỗ trợ:** ```chương hỗ trợ```
    - **Tạo số lượng câu hỏi cho keyword bất kì:** ```keyword: [keyword]: [số lượng câu hỏi (tối đa 10)]```  
  **Lưu ý:** Vì một số lý do nên hiện tại chatbot chỉ hỗ trợ sinh 10 câu hỏi cho mỗi keyword, vui lòng sử dụng nhiều keyword khác qua nhiều lần chat để sinh được đa dạng câu hỏi hơn.





