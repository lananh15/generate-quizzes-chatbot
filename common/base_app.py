from flask import Flask, render_template
from flask_cors import CORS
import openai
from typing import List
import tiktoken
import os
from flask import jsonify, request

class OpenAIHandlerBase:
    def __init__(self, api_key):
        self.api_key = api_key
        self.openai = openai
        self.openai.api_key = api_key

    # Khởi tạo cuộc trò chuyện với OpenAI
    def _call_openai_api(self, prompt: str) -> str:
        response = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Bạn là một trợ lý AI chuyên tạo câu hỏi trắc nghiệm cho môn học 'Quản lý dự án' dựa trên nội dung được cung cấp."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=0,
        )
        return response.choices[0].message['content']

    # Gửi thẳng nội dung lên openai mà không cần chia chunk vì nội dung nhỏ hơn 3800 tokens
    def _generate_questions_direct(self, content: str, num_questions: int) -> List[str]:
        prompt = self._build_prompt(num_questions, content, [])
        response = self._call_openai_api(prompt)
        questions = response.split('\n\n')
        return [q.strip() for q in questions if q.strip().startswith("Câu hỏi:")]

    # Xây dựng câu prompt để sinh ra quizz
    def _build_prompt(self, num_questions: int, content: str, keywords: List[str]) -> str:
        return f"""Tạo {num_questions} câu hỏi trắc nghiệm dựa trên nội dung sau. Tuân thủ các quy tắc sau:
        1. Mỗi câu hỏi bắt đầu bằng "Câu hỏi:" (không có số).
        2. Sau "Câu hỏi:" là nội dung đầy đủ của câu hỏi.
        3. Mỗi câu hỏi có 4 lựa chọn, bắt đầu bằng A, B, C, D. Tất cả các lựa chọn phải được hiển thị đầy đủ.
        4. Cuối mỗi câu hỏi, chỉ ra đáp án đúng bằng cách viết "Đáp án: [chữ cái]".
        5. Các câu hỏi được phân tách bằng một dòng trống.
        6. Tập trung vào chủ đề chính: {', '.join(keywords)}
        7. Đảm bảo rằng các câu hỏi liên quan trực tiếp đến nội dung và chủ đề được cung cấp, tuyệt đối không được tự chế ra thêm nội dung.

        Nội dung:
        {content}

        Chủ đề chính: {', '.join(keywords)}

        Ví dụ format:
        Câu hỏi: Nội dung đầy đủ của câu hỏi ở đây?
        A. Lựa chọn A
        B. Lựa chọn B
        C. Lựa chọn C
        D. Lựa chọn D
        Đáp án: B
        """
    
    # Đếm số lượng token trong nội dung
    def _count_tokens(self, text: str) -> int:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))


class QuizzSearchAppBase:
    def __init__(self, openai_handler):
        self.app = Flask(__name__, template_folder='../common/templates', static_folder='../common/static')
        CORS(self.app)
        self.openai_handler = openai_handler
        
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/chat', 'chat', self.chat, methods=['POST'])

    def index(self):
        return render_template('index.html')

    # Xử lý các cú pháp trong chatbot
    def chat(self):
        message = request.form['message']

        if message.lower() == 'chương hỗ trợ':
            return self._handle_chapter_structure()
        elif message.lower().startswith('chapter:'):
            return self._handle_questions(message, 'chapter', 25)
        elif message.lower().startswith('heading:'):
            return self._handle_questions(message, 'heading', 15)
        elif message.lower().startswith('subheading:'):
            return self._handle_questions(message, 'subheading', 10)
        elif message.lower().startswith('subsubheading:'):
            return self._handle_questions(message, 'subsubheading', 5)
        # Chỉ dùng cho pinecone với raw data
        elif message.lower().startswith('keyword:'):
            return self._handle_questions_with_keyword(message,10)
        
        else:
            return jsonify({"response": "Cú pháp không hợp lệ. Vui lòng thử lại."})

    # Tìm và in ra các chương được hỗ trợ
    def _handle_chapter_structure(self):
        raise NotImplementedError

    def find_excel_file(self, filename):
        for root, dirs, files in os.walk('/'):  # Bắt đầu tìm từ thư mục gốc
            if filename in files:
                return os.path.join(root, filename)
        return None

    # Xử lý các cú pháp search của người dùng
    def _handle_questions(self, message, question_type, max_questions):
        raise NotImplementedError
    
    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=5000)
