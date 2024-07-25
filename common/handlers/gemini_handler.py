from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiHandler:
    def __init__(self, api_key):
        self.llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-pro")

    def invoke(self, messages):
        return self.llm.invoke(messages)