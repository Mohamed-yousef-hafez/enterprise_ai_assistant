import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# استيراد الوظائف من الملفات السابقة
from rag_pipeline import init_vector_collection, ingest_documents
from sql_tool import init_sqlite_db
from agent_controller import run_agent

load_dotenv()

app = FastAPI(
    title="Enterprise Knowledge & Operations Assistant API",
    description="Advanced RAG and Autonomous Agent API built with LangGraph and FastAPI",
    version="1.0.0"
)

# نموذج البيانات المدخلة من المستخدم (Request Body)
class QueryRequest(BaseModel):
    question: str

# نموذج البيانات الخارجة (Response Body)
class QueryResponse(BaseModel):
    question: str
    answer: str

@app.on_event("startup")
def startup_event():
    """تهيئة قواعد البيانات عند بدء تشغيل السيرفر"""
    print("Initializing databases and vector stores...")
    init_vector_collection()
    init_sqlite_db()
    
    # اختيارية: تحميل بيانات تجريبية للـ RAG إذا وجد الملف
    sample_txt = "sample_data.txt"
    if os.path.exists(sample_txt):
        ingest_documents(sample_txt)
    print("System is ready!")

@app.get("/")
def read_root():
    """فحص حالة السيرفر"""
    return {"status": "Enterprise Agent API is running successfully!"}

@app.post("/chat", response_model=QueryResponse)
def chat_with_agent(request: QueryRequest):
    """الـ Endpoint الرئيسية لتلقي أسئلة المستخدم وتوجيهها للـ Agent"""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    try:
        # تشغيل الـ Agent الذي قمنا ببنائه في Sprint 3
        answer = run_agent(request.question)
        return QueryResponse(
            question=request.question,
            answer=answer
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")