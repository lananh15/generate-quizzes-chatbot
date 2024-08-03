from common.handlers.llm_handler_base import LLMHandlerBase
from typing import List, Dict, Tuple
import random

class ContentProcessor(LLMHandlerBase):
    # Tạo ra danh sách các câu hỏi dựa trên nội dung đầu vào
    def generate_questions(self, pinecone_results: List[Dict], num_questions: int) -> List[str]:
        all_content = self._combine_content(pinecone_results)
        print(all_content)
        if self._count_tokens(all_content) <= 3800:
            return self._generate_questions_direct(all_content, num_questions)
        else:
            return self._generate_questions_chunked(pinecone_results, num_questions)

    # Tổng hợp các câu hỏi có được sau mỗi chunk
    def _generate_questions_chunked(self, pinecone_results: List[Dict], num_questions: int) -> List[str]:
        all_questions = []
        chunks = self._chunk_content(pinecone_results)
        
        for chunk, metadata in chunks:
            chunk_questions = self._generate_questions_for_chunk(chunk, 5, metadata)
            all_questions.extend(chunk_questions)
        
        if len(all_questions) < num_questions:
            full_content = "\n\n".join([chunk for chunk, _ in chunks])
            full_metadata = {k: v for d in [metadata for _, metadata in chunks] for k, v in d.items()}
            additional_questions = self._generate_questions_for_chunk(full_content, num_questions - len(all_questions), full_metadata)
            all_questions.extend(additional_questions)
        
        random.shuffle(all_questions)
        return all_questions[:num_questions]

    # Gửi nội dung từ các chunk để sinh câu hỏi
    def _generate_questions_for_chunk(self, content: str, num_questions: int, metadata: Dict[str, str]) -> List[str]:
        context = self._build_context(metadata, content)
        prompt = self._build_prompt(num_questions, context)
        llm = self.get_llm()
        response = llm.invoke(prompt)
        print(f"\n\nModel được dùng: {llm}")
        questions = response.content.split('\n\n')
        return [q.strip() for q in questions if q.strip().startswith("Câu hỏi:")]

    # Chia nội dung ra thành các chunk nếu nội dung quá dài
    def _chunk_content(self, pinecone_results: List[Dict]) -> List[str]:
        chunks = []
        for result in pinecone_results:
            metadata = result.get('metadata', {})
            content = metadata.get('text', '')
            
            # Thêm nội dung vào danh sách chunks
            chunks.append(content)
            
        return chunks

    def _build_context(self, result: Dict[str, Dict[str, str]]) -> str:
        content = result['metadata'].get('text', '')
        return f"Content: {content}"

    # Kết hợp nội dung từ nhiều kết quả tìm kiếm Pinecone thành một chuỗi văn bản tổng hợp
    def _combine_content(self, pinecone_results: List[Dict]) -> str:
        contents = []
        for result in pinecone_results:
            metadata = result['metadata']
            content = metadata.get('text', '')
            contents.append(content)
        return "\n\n".join(contents)