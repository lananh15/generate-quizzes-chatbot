
## :computer: Dùng chatbot hỗ trợ sinh câu hỏi (sử dụng Pinecone với dữ liệu có cấu trúc)
**1. Lưu cấu trúc dữ liệu từ file .json lên Pinecone**  
  - Run file **save_structured_data_to_pinecone.py** để có thể lưu dữ liệu từ file **qtda.json** lên Pinecone theo các vector, chatbot sẽ sử dụng dữ liệu trên Pinecone để tạo câu hỏi cho môn học.  

**2. Sử dụng chatbot**  
  - Run file **app.py** và truy cập vào http://127.0.0.1:5000/ để dùng chatbot ở localhost.
  - Các cú pháp để dùng chatbot:  
    - **Xem cấu trúc chương, tiêu đề chính, tiêu đề phụ, tiểu mục của môn học mà chúng tôi hỗ trợ:** ```chương hỗ trợ```
    - **Tạo số lượng câu hỏi cho chương bất kì:** ```chapter: [tên chương]: [số lượng câu hỏi (tối đa 25)]```  
    - **Tạo số lượng câu hỏi cho tiêu đề chính bất kì:** ```heading: [tên tiêu đề chính]: [số lượng câu hỏi (tối đa 15)]```  
    - **Tạo số lượng câu hỏi cho tiêu đề phụ bất kì:** ```subheading: [tên tiêu đề phụ]: [số lượng câu hỏi (tối đa 10)]```  
    - **Tạo số lượng câu hỏi cho tiểu mục bất kì:** ```subsubheading: [tên tiểu mục]: [số lượng câu hỏi (tối đa 5)]```  

**Lưu ý:** Bạn cũng có thể thay đổi API key, tên index khác từ tài khoản Pinecone và sử dụng openai_api_key của riêng bạn.  
  - Để làm được, bạn cần phải có tài khoản trên https://www.pinecone.io/ và tạo index. Sau đó thay đổi các giá trị **api_key**, **index_name**, **dimension** (nếu dùng mô hình text-embedding-ada-002 của openAI thì giữ nguyên 1536), **cloud** và **region** trong đoạn code dưới đây của file **save_structured_data_to_pinecone.py** sao cho phù hợp.
  ```
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
  ```
    if __name__ == '__main__':
    openai_handler = PineconeOpenAIHandler("sk-proj-e3BgNgIvICywLYluJyeUT3BlbkFJenYTISe35HiZEiki9Gz3")
    pc = Pinecone(api_key="020a8257-5dd3-41f3-a710-53d7c6fac5d9")
    index = pc.Index("generate-quizz")
    app = PineconeQuizzSearchApp(openai_handler, index)
    app.run()
    ```





