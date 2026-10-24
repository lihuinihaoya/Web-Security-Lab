from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_chroma import Chroma

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 本地大模型初始化
llm = OllamaLLM(model="modelscope.cn/Qwen/Qwen2.5-7B-Instruct-GGUF:latest")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

@app.get("/ask")
def ask_ai(question: str):
    # 这里省略了建库过程，仅作代码展示
    return {"answer": f"这是针对问题的回答: {question}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
