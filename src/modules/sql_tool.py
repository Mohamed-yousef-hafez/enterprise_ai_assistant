import sqlite3
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

DB_FILE = "enterprise_data.db"

def init_sqlite_db():
    """إنشاء قاعدة بيانات تجريبية تحتوي على جدول للشكاوى والطلبات"""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # إنشاء جدول الشكاوى
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT,
        department TEXT,
        issue_type TEXT,
        status TEXT,
        date_filed TEXT
    )
    """)
    
    # إدخال بيانات تجريبية
    sample_data = [
        ("أحمد محمد", "IT", "مشكلة في خادم الدعم", "معلق", "2026-05-10"),
        ("سارة علي", "HR", "طلب إجازة سنوية", "تم الحل", "2026-05-12"),
        ("محمود حسن", "Finance", "تأخر صرف المستحقات", "قيد المراجعة", "2026-05-15")
    ]
    cursor.executemany("INSERT INTO complaints (employee_name, department, issue_type, status, date_filed) VALUES (?, ?, ?, ?, ?)", sample_data)
    
    conn.commit()
    conn.close()
    print("SQLite Database initialized with sample data.")

def query_database(sql_query: str):
    """تنفيذ استعلام SQL بشكل آمن وإرجاع النتائج"""
    # حماية بسيطة للتأكد من أن الاستعلام استعلام قراءة (SELECT) فقط
    if not sql_query.strip().upper().startswith("SELECT"):
        return "Error: Only SELECT queries are allowed for security reasons."
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        
        # تحويل النتائج إلى شكل نصي مفيد للـ Agent
        results = [dict(zip(columns, row)) for row in rows]
        return str(results)
    except Exception as e:
        return f"SQL Error: {str(e)}"

def text_to_sql_agent_tool(natural_language_query: str) -> str:
    """تحويل لغة المستخدم العادية إلى SQL ثم تنفيذها"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    schema_info = """
    Table: complaints
    Columns:
    - id (INTEGER)
    - employee_name (TEXT)
    - department (TEXT)
    - issue_type (TEXT)
    - status (TEXT - e.g., 'معلق', 'تم الحل', 'قيد المراجعة')
    - date_filed (TEXT)
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an SQL expert. Given the database schema, write a valid SQLite SELECT query to answer the user's question. Return ONLY the raw SQL query without any markdown formatting or extra text.\n\nSchema:\n{schema}"),
        ("user", "{query}")
    ])
    
    chain = prompt | llm
    sql_query = chain.invoke({"schema": schema_info, "query": natural_language_query}).content.strip()
    
    # تنظيف أي فواصل كود إضافية إن وجدت
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
    
    print(f"[Generated SQL]: {sql_query}")
    return query_database(sql_query)