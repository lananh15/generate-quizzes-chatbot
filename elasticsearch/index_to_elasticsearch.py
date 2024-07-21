from elasticsearch import Elasticsearch
import json
import os

# Thiết lập kết nối tới Elasticsearch (chỉnh sửa host và port nếu cần thiết)
es = Elasticsearch(['http://localhost:9200'])

script_dir = os.path.dirname(__file__)  # Thư mục chứa script Python hiện tại
json_file = os.path.join(script_dir, '..', 'data', 'qtda.json')
json_file = os.path.abspath(json_file)

# Đọc dữ liệu từ file JSON
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Mapping đã thiết lập cho index
index_mapping = {
    "mappings": {
        "properties": {
            "chapters": {
                "type": "nested",
                "properties": {
                    "title": {"type": "text"},
                    "headings": {
                        "type": "nested",
                        "properties": {
                            "title": {"type": "text"},
                            "content": {"type": "text"},
                            "keywords": {"type": "text"},
                            "subheadings": {
                                "type": "nested",
                                "properties": {
                                    "title": {"type": "text"},
                                    "content": {"type": "text"},
                                    "keywords": {"type": "text"},
                                    "subsubheadings": {
                                        "type": "nested",
                                        "properties": {
                                            "title": {"type": "text"},
                                            "content": {"type": "text"},
                                            "keywords": {"type": "text"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

# Tên index trong Elasticsearch
index_name = 'qtda'

# Xóa index nếu tồn tại
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# Tạo index mới với mapping đã thiết lập
es.indices.create(index=index_name, body=index_mapping)

# Lưu dữ liệu vào Elasticsearch
for doc_id, doc in enumerate(data['chapters']):
    es.index(index=index_name, id=doc_id, body=doc)

print(f"Indexed {len(data['chapters'])} documents into '{index_name}' index.")
