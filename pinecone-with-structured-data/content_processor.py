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
        prompt = self._build_prompt(num_questions, content, metadata.get('keywords', []))
        llm = self.get_llm()
        response = llm.invoke(prompt)
        print(f"\n\nModel được dùng: {llm}")
        questions = response.content.split('\n\n')
        return [q.strip() for q in questions if q.strip().startswith("Câu hỏi:")]

    # Chia nội dung ra thành các chunk nếu nội dung quá dài
    def _chunk_content(self, pinecone_results: List[Dict]) -> List[Tuple[str, Dict[str, str]]]:
        chunks = []
        for result in pinecone_results:
            metadata = result['metadata']
            chunk_metadata = {k: metadata.get(k, '') for k in ['chapter_title', 'heading_title', 'subheading_title', 'subsubheading_title', 'keywords']}
            
            if 'chapter_title' in metadata:
                chapter_title = metadata['chapter_title']
                for content_type in ['heading', 'subheading', 'subsubheading']:
                    title_key = f'{content_type}_title'
                    content_key = f'{content_type}_content'
                    if title_key in metadata and content_key in metadata:
                        chunks.append((f"Chapter: {chapter_title}\n{content_type.capitalize()}: {metadata[title_key]}\nContent: {metadata[content_key]}", chunk_metadata))
        
        return chunks

    # Tạo một chuỗi văn bản mô tả ngữ cảnh dựa trên các thông tin từ metadata và nội dung đầu vào
    def _build_context(self, metadata: Dict[str, str], content: str) -> str:
        context = f"Chapter: {metadata.get('chapter_title', '')}\n"
        for title_type in ['heading', 'subheading']:
            if metadata.get(f'{title_type}_title'):
                context += f"{title_type.capitalize()}: {metadata[f'{title_type}_title']}\n"
        context += f"Keywords: {', '.join(metadata.get('keywords', []))}\n"
        context += f"Content: {content}"
        return context

    # Kết hợp nội dung từ nhiều kết quả tìm kiếm Pinecone thành một chuỗi văn bản tổng hợp
    def _combine_content(self, pinecone_results: List[Dict]) -> str:
        contents = []
        for result in pinecone_results:
            metadata = result['metadata']
            content = f"Chapter: {metadata.get('chapter_title', '')}\n"
            
            if 'heading_title' in metadata:
                content += f"Heading: {metadata['heading_title']}\n"
            if 'subheading_title' in metadata:
                content += f"Subheading: {metadata['subheading_title']}\n"
            if 'subsubheading_title' in metadata:
                content += f"Subsubheading: {metadata['subsubheading_title']}\n"
            
            # Tạo một danh sách để lưu trữ tất cả các loại nội dung
            content_parts = []
            if 'subsubheading_content' in metadata:
                content_parts.append(metadata['subsubheading_content'])
            if 'subheading_content' in metadata:
                content_parts.append(metadata['subheading_content'])
            if 'heading_content' in metadata:
                content_parts.append(metadata['heading_content'])
            if 'content' in metadata:
                content_parts.append(metadata['content'])
            
            # Kết hợp tất cả các phần nội dung
            content += "Content:\n" + "\n".join(content_parts) + "\n\n"
            contents.append(content)
        
        return "\n".join(contents)

