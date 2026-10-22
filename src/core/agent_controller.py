import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# استيراد الوظائف من الملفات السابقة
from rag_pipeline import hybrid_search
from sql_tool import text_to_sql_agent_tool

load_dotenv()

# 1. تحويل وظائف الـ RAG والـ SQL إلى أدوات (Tools) يفهمها الـ Agent
@tool
def search_company_documents(query: str) -> str:
    """Useful for searching company policies, handbooks, text documents, and general guidelines using semantic search."""
    results = hybrid_search(query, limit=3)
    if not results:
        return "No relevant documents found."
    
    formatted_output = ""
    for r in results:
        formatted_output += f"- {r['content']}\n"
    return formatted_output

@tool
def query_company_database(natural_language_query: str) -> str:
    """Useful for answering questions about structured data like employees, complaints, statuses, and operational logs stored in the SQL database. Pass the user's natural language question directly."""
    result = text_to_sql_agent_tool(natural_language_query)
    return str(result)

# 2. تجميع الأدوات في قائمة واحدة
tools = [search_company_documents, query_company_database]

# 3. إعداد نموذج الـ LLM الخاص بالـ Agent
model = ChatOpenAI(model="gpt-4o", temperature=0)

# 4. بناء الـ ReAct Agent باستخدام LangGraph
# الـ LangGraph prebuilt agent يدير دورة التفكير (Thought -> Action -> Observation -> Answer) تلقائياً
agent_executor = create_react_agent(model, tools)

def run_agent(user_question: str):
    """دالة لتشغيل الـ Agent واستقبال سؤال المستخدم"""
    print(f"\n[User Question]: {user_question}")
    print("Agent is thinking and selecting tools...\n")
    
    # استدعاء الـ Agent بالرسالة
    messages = {"messages": [("user", user_question)]}
    response = agent_executor.invoke(messages)
    
    # استخراج الإجابة النهائية من آخر رسالة في الـ State
    final_answer = response["messages"][-1].content
    return final_answer

if __name__ == "__main__":
    # اختبار سريع للـ Agent (تأكد من تهيئة قاعدة البيانات وملف الـ sample مسبقاً)
    # query = "ما هي حالة شكوى الموظف أحمد محمد؟"
    # print(run_agent(query))
    pass