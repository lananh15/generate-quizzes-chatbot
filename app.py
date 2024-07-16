# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS
# import json
# import openai
# from typing import List, Dict, Tuple
# from pinecone import Pinecone
# import random

# class OpenAIHandler:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         self.openai = openai
#         self.openai.api_key = api_key

#     def generate_questions(self, pinecone_results: List[Dict], num_questions: int) -> List[str]:
#         all_questions = []
#         chunks = self._chunk_content(pinecone_results)
        
#         for chunk, metadata in chunks:
#             chunk_questions = self.generate_questions_chunk(chunk, 5, metadata)  # Tạo 5 câu hỏi cho mỗi chunk
#             all_questions.extend(chunk_questions)
        
#         # Nếu chưa đủ câu hỏi, tiếp tục tạo thêm
#         if len(all_questions) < num_questions:
#             full_content = "\n\n".join([chunk for chunk, _ in chunks])
#             full_metadata = {k: v for d in [metadata for _, metadata in chunks] for k, v in d.items()}
#             additional_questions = self.generate_questions_chunk(full_content, num_questions - len(all_questions), full_metadata)
#             all_questions.extend(additional_questions)
        
#         # Trộn tất cả các câu hỏi và chọn số câu hỏi cần thiết
#         random.shuffle(all_questions)
#         selected_questions = all_questions[:num_questions]
        
#         return selected_questions

#     def generate_questions_chunk(self, content: str, num_questions: int, metadata: Dict[str, str]) -> List[str]:
#         chapter_title = metadata.get('chapter_title', '')
#         heading_title = metadata.get('heading_title', '')
#         subheading_title = metadata.get('subheading_title', '')
#         keywords = metadata.get('keywords', [])

#         context = f"Chapter: {chapter_title}\n"
#         if heading_title:
#             context += f"Heading: {heading_title}\n"
#         if subheading_title:
#             context += f"Subheading: {subheading_title}\n"
#         context += f"Keywords: {', '.join(keywords)}\n"
#         context += f"Content: {content}"

#         prompt = f"""Tạo {num_questions} câu hỏi trắc nghiệm dựa trên nội dung sau. Tuân thủ các quy tắc sau:
#         1. Mỗi câu hỏi bắt đầu bằng "Câu hỏi:" (không có số).
#         2. Sau "Câu hỏi:" là nội dung đầy đủ của câu hỏi.
#         3. Mỗi câu hỏi có 4 lựa chọn, bắt đầu bằng A, B, C, D. Tất cả các lựa chọn phải được hiển thị đầy đủ.
#         4. Cuối mỗi câu hỏi, chỉ ra đáp án đúng bằng cách viết "Đáp án: [chữ cái]".
#         5. Các câu hỏi được phân tách bằng một dòng trống.
#         6. Tập trung vào chủ đề chính: {', '.join(keywords)}
#         7. Đảm bảo rằng các câu hỏi liên quan trực tiếp đến nội dung và chủ đề được cung cấp, tuyệt đối không được tự chế ra thêm nội dung.

#         Nội dung:
#         {content}

#         Chủ đề chính: {', '.join(keywords)}

#         Ví dụ format:
#         Câu hỏi: Nội dung đầy đủ của câu hỏi ở đây?
#         A. Lựa chọn A
#         B. Lựa chọn B
#         C. Lựa chọn C
#         D. Lựa chọn D
#         Đáp án: B

#         """
        
#         response = self.openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": "Bạn là một trợ lý AI chuyên tạo câu hỏi trắc nghiệm cho môn học 'Quản lý dự án'."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=2000,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )
        
#         questions = response.choices[0].message['content'].split('\n\n')
#         return [q.strip() for q in questions if q.strip().startswith("Câu hỏi:")]

#     def _chunk_content(self, pinecone_results: List[Dict]) -> List[Tuple[str, Dict[str, str]]]:
#         chunks = []
#         for result in pinecone_results:
#             metadata = result['metadata']
#             chunk_metadata = {
#                 'chapter_title': metadata.get('chapter_title', ''),
#                 'heading_title': metadata.get('heading_title', ''),
#                 'subheading_title': metadata.get('subheading_title', ''),
#                 'subsubheading_title': metadata.get('subsubheading_title', ''),
#                 'keywords': metadata.get('keywords', [])
#             }
            
#             if 'chapter_title' in metadata:
#                 chapter_title = metadata['chapter_title']
                
#                 if 'heading_title' in metadata and 'heading_content' in metadata:
#                     heading_title = metadata['heading_title']
#                     heading_content = metadata['heading_content']
#                     chunks.append((f"Chapter: {chapter_title}\nHeading: {heading_title}\nContent: {heading_content}", chunk_metadata))
                
#                 if 'subheading_title' in metadata and 'subheading_content' in metadata:
#                     subheading_title = metadata['subheading_title']
#                     subheading_content = metadata['subheading_content']
#                     chunks.append((f"Chapter: {chapter_title}\nSubheading: {subheading_title}\nContent: {subheading_content}", chunk_metadata))
                
#                 if 'subsubheading_title' in metadata and 'subsubheading_content' in metadata:
#                     subsubheading_title = metadata['subsubheading_title']
#                     subsubheading_content = metadata['subsubheading_content']
#                     chunks.append((f"Chapter: {chapter_title}\nSubsubheading: {subsubheading_title}\nContent: {subsubheading_content}", chunk_metadata))
        
#         return chunks


# class QuizzSearchApp:
#     def __init__(self, openai_handler, pinecone_index):
#         self.app = Flask(__name__)
#         CORS(self.app)
#         self.openai_handler = openai_handler
#         self.pinecone_handler = pinecone_index
        
#         self.app.add_url_rule('/', 'index', self.index)
#         self.app.add_url_rule('/chat', 'chat', self.chat, methods=['POST'])

#     def index(self):
#         return render_template('index.html')

#     def get_chapter_structure_from_pinecone(self):
#         query_embedding = self.openai_handler.openai.Embedding.create(
#             input="chapter_title",
#             model="text-embedding-ada-002"
#         )['data'][0]['embedding']
        
#         result = self.pinecone_handler.query(
#             vector=query_embedding,
#             top_k=100, 
#             include_metadata=True
#         )
        
#         chapter_structure = {}
#         for match in result['matches']:
#             metadata = match['metadata']
#             chapter_title = metadata.get('chapter_title')
#             if chapter_title:
#                 if chapter_title not in chapter_structure:
#                     chapter_structure[chapter_title] = {'headings': {}}
                
#                 heading_title = metadata.get('heading_title')
#                 if heading_title:
#                     if heading_title not in chapter_structure[chapter_title]['headings']:
#                         chapter_structure[chapter_title]['headings'][heading_title] = {'subheadings': {}}
                    
#                     subheading_title = metadata.get('subheading_title')
#                     if subheading_title:
#                         if subheading_title not in chapter_structure[chapter_title]['headings'][heading_title]['subheadings']:
#                             chapter_structure[chapter_title]['headings'][heading_title]['subheadings'][subheading_title] = []
                        
#                         subsubheading_title = metadata.get('subsubheading_title')
#                         if subsubheading_title:
#                             chapter_structure[chapter_title]['headings'][heading_title]['subheadings'][subheading_title].append(subsubheading_title)
        
#         return chapter_structure

#     def search_pinecone(self, query: str, number: int) -> List[Dict]:
#         query_embedding = self.openai_handler.openai.Embedding.create(
#             input=query,
#             model="text-embedding-ada-002"
#         )['data'][0]['embedding']
        
#         result = self.pinecone_handler.query(
#             vector=query_embedding,
#             top_k=number,
#             include_metadata=True
#         )
        
#         # Sắp xếp kết quả, ưu tiên các vector có keyword trùng khớp
#         sorted_results = sorted(result['matches'], key=lambda x: query.lower() in [k.lower() for k in x['metadata'].get('keywords', [])], reverse=True)
        
#         print(f"Search results for query '{query}':")
#         for i, match in enumerate(sorted_results, 1):
#             print(f"Match {i}:")
#             print(f"  Score: {match['score']}")
#             print(f"  Metadata: {match['metadata']}")
#             print("---")
#         return sorted_results

#     def chat(self):
#         message = request.form['message']

#         if message.lower() == 'chương':
#             chapter_structure = self.get_chapter_structure_from_pinecone()
#             response = "Các chương được hỗ trợ:\n\n"
#             for idx, (chapter_title, chapter_data) in enumerate(chapter_structure.items(), start=1):
#                 response += f"{idx}. {chapter_title}"
#                 for heading_title, heading_data in chapter_data['headings'].items():
#                     response += f"- {heading_title}"
#                     for subheading_title, subsubheadings in heading_data['subheadings'].items():
#                         response += f"+ {subheading_title}"
#                         for subsubheading in subsubheadings:
#                             response += f"* {subsubheading}"
#                 response += "\n"
#             response += "\nBạn có thể nhập <code>`câu hỏi chương: [tên chương]: [số lượng câu hỏi (tối đa 25)]`</code> hoặc <code>`câu hỏi phần: [tên phần]: [số lượng câu hỏi (tối đa 10)]`</code> để tạo số lượng câu hỏi cho chương hoặc 1 phần cụ thể bạn cần."

#             # Thêm định dạng HTML để cải thiện hiển thị
#             response = response.replace("\n", "<br>")
#             response = response.replace("- ", "<br>&nbsp;&nbsp;- ")
#             response = response.replace("+ ", "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ ")
#             response = response.replace("* ", "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* ")    

#         elif message.lower().startswith('câu hỏi chương:'):
#             parts = message.split(':')
#             if len(parts) == 3:
#                 chapter_title = parts[1].strip()
#                 try:
#                     num_questions = int(parts[2].strip())
#                     if num_questions <= 0:
#                         response = "Số lượng câu hỏi phải là số dương."
#                     elif num_questions > 25:
#                         response = "Chỉ được chọn tối đa 25 câu hỏi cho mỗi chương."
#                     else:
#                         pinecone_results = self.search_pinecone(chapter_title,8)
#                         all_questions = self.openai_handler.generate_questions(pinecone_results, num_questions)
                        
#                         response = f"{num_questions} câu hỏi của chương '{chapter_title}':\n\n"
#                         for i, question in enumerate(all_questions, 1):
#                             response += f"{i}. {question}\n----------\n"
#                 except ValueError:
#                     response = "Số lượng câu hỏi phải là một số nguyên."
#             else:
#                 response = "Vui lòng nhập theo định dạng: <code>'câu hỏi chương: [tên chương]: [số lượng câu hỏi (tối đa 25)]'</code>."

#         elif message.lower().startswith('câu hỏi phần:'):
#             parts = message.split(':')
#             if len(parts) == 3:
#                 heading_title = parts[1].strip()
#                 try:
#                     num_questions = int(parts[2].strip())
#                     if num_questions <= 0:
#                         response = "Số lượng câu hỏi phải là số dương."
#                     elif num_questions > 8:
#                         response = "Chỉ được chọn tối đa 8 câu hỏi cho mỗi phần."
#                     else:
#                         pinecone_results = self.search_pinecone(heading_title, 2)
#                         matched_results = [result for result in pinecone_results if heading_title.lower() in [k.lower() for k in result['metadata'].get('keywords', [])]]
                
#                         # Nếu có kết quả trùng khớp, sử dụng chúng; nếu không, sử dụng tất cả kết quả
#                         results_to_use = matched_results if matched_results else pinecone_results
#                         print(results_to_use)
#                         all_questions = self.openai_handler.generate_questions(results_to_use, num_questions)
                        
#                         response = f"{num_questions} câu hỏi của phần '{heading_title}':\n\n"
#                         for i, question in enumerate(all_questions, 1):
#                             response += f"{i}. {question}\n----------\n"
#                 except ValueError:
#                     response = "Số lượng câu hỏi phải là một số nguyên."
#             else:
#                 response = "Vui lòng nhập theo định dạng: <code>`câu hỏi phần: [tên phần]: [số lượng câu hỏi (tối đa 8)]`</code>."
#         else:
#             response = "Cú pháp không hợp lệ. Vui lòng thử lại."
        
#         return jsonify({"response": response})

#     def run(self):
#         self.app.run(debug=True, host="0.0.0.0", port=5000)

# if __name__ == '__main__':
#     openai_handler = OpenAIHandler("sk-proj-e3BgNgIvICywLYluJyeUT3BlbkFJenYTISe35HiZEiki9Gz3")
#     pc = Pinecone(api_key="020a8257-5dd3-41f3-a710-53d7c6fac5d9")
#     index = pc.Index("generate-quizz")
#     app = QuizzSearchApp(openai_handler, index)
#     app.run()

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
from typing import List, Dict, Tuple
from pinecone import Pinecone
import random
import tiktoken

class OpenAIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.openai = openai
        self.openai.api_key = api_key

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
            temperature=0.7,
        )
        return response.choices[0].message['content']
    
    def generate_questions(self, pinecone_results: List[Dict], num_questions: int) -> List[str]:
        all_content = self._combine_content(pinecone_results)
        
        if self._count_tokens(all_content) <= 3900:
            return self._generate_questions_direct(all_content, num_questions)
        else:
            return self._generate_questions_chunked(pinecone_results, num_questions)

    def _generate_questions_direct(self, content: str, num_questions: int) -> List[str]:
        prompt = self._build_prompt(num_questions, content, [])
        response = self._call_openai_api(prompt)
        questions = response.split('\n\n')
        return [q.strip() for q in questions if q.strip().startswith("Câu hỏi:")]

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

    def _generate_questions_for_chunk(self, content: str, num_questions: int, metadata: Dict[str, str]) -> List[str]:
        context = self._build_context(metadata, content)
        prompt = self._build_prompt(num_questions, content, metadata.get('keywords', []))
        response = self._call_openai_api(prompt)
        questions = response.split('\n\n')
        return [q.strip() for q in questions if q.strip().startswith("Câu hỏi:")]

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

    def _build_context(self, metadata: Dict[str, str], content: str) -> str:
        context = f"Chapter: {metadata.get('chapter_title', '')}\n"
        for title_type in ['heading', 'subheading']:
            if metadata.get(f'{title_type}_title'):
                context += f"{title_type.capitalize()}: {metadata[f'{title_type}_title']}\n"
        context += f"Keywords: {', '.join(metadata.get('keywords', []))}\n"
        context += f"Content: {content}"
        return context

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
            content += f"Content: {metadata.get('content', '')}\n\n"
            contents.append(content)
        return "\n".join(contents)

    def _count_tokens(self, text: str) -> int:
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        return len(encoding.encode(text))

class QuizzSearchApp:
    def __init__(self, openai_handler, pinecone_index):
        self.app = Flask(__name__)
        CORS(self.app)
        self.openai_handler = openai_handler
        self.pinecone_handler = pinecone_index
        
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/chat', 'chat', self.chat, methods=['POST'])

    def index(self):
        return render_template('index.html')

    def get_chapter_structure_from_pinecone(self):
        query_embedding = self.openai_handler.openai.Embedding.create(
            input="chapter_title",
            model="text-embedding-ada-002"
        )['data'][0]['embedding']
        
        result = self.pinecone_handler.query(
            vector=query_embedding,
            top_k=100, 
            include_metadata=True
        )
        
        chapter_structure = {}
        for match in result['matches']:
            metadata = match['metadata']
            chapter_title = metadata.get('chapter_title')
            if chapter_title:
                if chapter_title not in chapter_structure:
                    chapter_structure[chapter_title] = {'headings': {}}
                
                heading_title = metadata.get('heading_title')
                if heading_title:
                    if heading_title not in chapter_structure[chapter_title]['headings']:
                        chapter_structure[chapter_title]['headings'][heading_title] = {'subheadings': {}}
                    
                    subheading_title = metadata.get('subheading_title')
                    if subheading_title:
                        if subheading_title not in chapter_structure[chapter_title]['headings'][heading_title]['subheadings']:
                            chapter_structure[chapter_title]['headings'][heading_title]['subheadings'][subheading_title] = []
                        
                        subsubheading_title = metadata.get('subsubheading_title')
                        if subsubheading_title:
                            chapter_structure[chapter_title]['headings'][heading_title]['subheadings'][subheading_title].append(subsubheading_title)
        
        return chapter_structure

    def search_pinecone(self, query: str, number: int) -> List[Dict]:
        query_embedding = self.openai_handler.openai.Embedding.create(
            input=query,
            model="text-embedding-ada-002"
        )['data'][0]['embedding']
        
        result = self.pinecone_handler.query(
            vector=query_embedding,
            top_k=number,
            include_metadata=True
        )
        
        sorted_results = sorted(result['matches'], key=lambda x: query.lower() in [k.lower() for k in x['metadata'].get('keywords', [])], reverse=True)
        
        print(f"Search results for query '{query}':")
        for i, match in enumerate(sorted_results, 1):
            print(f"Match {i}:")
            print(f"  Score: {match['score']}")
            print(f"  Metadata: {match['metadata']}")
            print("---")
        return sorted_results

    def chat(self):
        message = request.form['message']

        if message.lower() == 'chương':
            return self._handle_chapter_structure()
        elif message.lower().startswith('câu hỏi chương:'):
            return self._handle_chapter_questions(message)
        elif message.lower().startswith('câu hỏi phần:'):
            return self._handle_section_questions(message)
        else:
            return jsonify({"response": "Cú pháp không hợp lệ. Vui lòng thử lại."})

    def _handle_chapter_structure(self):
        chapter_structure = self.get_chapter_structure_from_pinecone()
        response = "Các chương được hỗ trợ:\n\n"
        for idx, (chapter_title, chapter_data) in enumerate(chapter_structure.items(), start=1):
            response += f"{idx}. {chapter_title}"
            for heading_title, heading_data in chapter_data['headings'].items():
                response += f"- {heading_title}"
                for subheading_title, subsubheadings in heading_data['subheadings'].items():
                    response += f"+ {subheading_title}"
                    for subsubheading in subsubheadings:
                        response += f"* {subsubheading}"
            response += "\n"
        response += "\nBạn có thể nhập <code>`câu hỏi chương: [tên chương]: [số lượng câu hỏi (tối đa 25)]`</code> hoặc <code>`câu hỏi phần: [tên phần]: [số lượng câu hỏi (tối đa 10)]`</code> để tạo số lượng câu hỏi cho chương hoặc 1 phần cụ thể bạn cần."

        response = response.replace("\n", "<br>")
        response = response.replace("- ", "<br>&nbsp;&nbsp;- ")
        response = response.replace("+ ", "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;+ ")
        response = response.replace("* ", "<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* ")    
        return jsonify({"response": response})

    def _handle_chapter_questions(self, message):
        parts = message.split(':')
        if len(parts) != 3:
            return jsonify({"response": "Vui lòng nhập theo định dạng: <code>'câu hỏi chương: [tên chương]: [số lượng câu hỏi (tối đa 25)]'</code>."})
        
        chapter_title = parts[1].strip()
        try:
            num_questions = int(parts[2].strip())
            if num_questions <= 0:
                return jsonify({"response": "Số lượng câu hỏi phải là số dương."})
            if num_questions > 25:
                return jsonify({"response": "Chỉ được chọn tối đa 25 câu hỏi cho mỗi chương."})
            
            pinecone_results = self.search_pinecone(chapter_title, 8)
            matched_results = [result for result in pinecone_results if chapter_title.lower() in result['metadata'].get('chapter_title', '').lower()]
            results_to_use = matched_results if matched_results else pinecone_results
            
            all_questions = self.openai_handler.generate_questions(results_to_use, num_questions)
        
            
            response = f"{num_questions} câu hỏi của chương '{chapter_title}':\n\n"
            for i, question in enumerate(all_questions, 1):
                response += f"{i}. {question}\n----------\n"
            return jsonify({"response": response})
        except ValueError:
            return jsonify({"response": "Số lượng câu hỏi phải là một số nguyên."})

    def _handle_section_questions(self, message):
        parts = message.split(':')
        if len(parts) != 3:
            return jsonify({"response": "Vui lòng nhập theo định dạng: <code>`câu hỏi phần: [tên phần]: [số lượng câu hỏi (tối đa 8)]`</code>."})
        
        heading_title = parts[1].strip()
        try:
            num_questions = int(parts[2].strip())
            if num_questions <= 0:
                return jsonify({"response": "Số lượng câu hỏi phải là số dương."})
            if num_questions > 8:
                return jsonify({"response": "Chỉ được chọn tối đa 8 câu hỏi cho mỗi phần."})
            
            pinecone_results = self.search_pinecone(heading_title, 2)
            matched_results = [result for result in pinecone_results if heading_title.lower() in [k.lower() for k in result['metadata'].get('keywords', [])]]
            results_to_use = matched_results if matched_results else pinecone_results
            print(results_to_use)
            all_questions = self.openai_handler.generate_questions(results_to_use, num_questions)
            
            response = f"{num_questions} câu hỏi của phần '{heading_title}':\n\n"
            for i, question in enumerate(all_questions, 1):
                response += f"{i}. {question}\n----------\n"
            return jsonify({"response": response})
        except ValueError:
            return jsonify({"response": "Số lượng câu hỏi phải là một số nguyên."})

    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=5000)

if __name__ == '__main__':
    openai_handler = OpenAIHandler("sk-proj-e3BgNgIvICywLYluJyeUT3BlbkFJenYTISe35HiZEiki9Gz3")
    pc = Pinecone(api_key="020a8257-5dd3-41f3-a710-53d7c6fac5d9")
    index = pc.Index("generate-quizz")
    app = QuizzSearchApp(openai_handler, index)
    app.run()