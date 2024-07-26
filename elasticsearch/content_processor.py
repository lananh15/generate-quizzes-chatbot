from common.handlers.llm_handler_base import LLMHandlerBase
from typing import List
import random

class ContentProcessor(LLMHandlerBase):
    # Tạo ra danh sách các câu hỏi dựa trên nội dung đầu vào
    def generate_questions(self, content: str, num_questions: int) -> List[str]:
        if self._count_tokens(content) <= 3800:
            print(content)
            return self._generate_questions_direct(content, num_questions)
        else:
            return self._generate_questions_chunked(content, num_questions)

    # Tổng hợp các câu hỏi có được sau mỗi chunk
    def _generate_questions_chunked(self, content: str, num_questions: int) -> List[str]:
        chunks = self._chunk_content(content)
        all_questions = []
        
        for chunk in chunks:
            chunk_questions = self._generate_questions_for_chunk(chunk, 8)  # tạo 8 câu hỏi cho mỗi chunk
            all_questions.extend(chunk_questions)
        
        random.shuffle(all_questions)
        return all_questions[:num_questions]
    
    # Gửi nội dung từ các chunk để sinh câu hỏi
    def _generate_questions_for_chunk(self, content: str, num_questions: int) -> List[str]:
        prompt = self._build_prompt(num_questions, content)
        llm = self.get_llm()
        response = llm.invoke(prompt)
        print(f"\n\nModel được dùng: {llm}")
        questions = response.content.split('\n\n')
        return [q.strip() for q in questions if q.strip().startswith("Câu hỏi:")]
    # Chia nội dung ra thành các chunk nếu nội dung quá dài
    def _chunk_content(self, content: str) -> List[str]:
        chunks = []
        current_chunk = ""
        for line in content.split('\n'):
            if self._count_tokens(current_chunk + line) > 3800:
                chunks.append(current_chunk)
                current_chunk = line
            else:
                current_chunk += line + '\n'
        if current_chunk:
            chunks.append(current_chunk)
        return chunks

