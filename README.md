# 🤖 Enterprise Knowledge & Operations Assistant

An advanced, production-ready Enterprise AI Assistant powered by **LangGraph**, **Advanced RAG (Hybrid Search + Re-ranking)**, and **Autonomous SQL/Action Agents**, wrapped in a **FastAPI** backend and a **Streamlit** frontend.

---

## 🏗️ System Architecture
The system routes user queries intelligently:
- **Natural Language Documents Search** $\rightarrow$ Handled by Hybrid RAG (Qdrant).
- **Structured Operations/Data Queries** $\rightarrow$ Handled by Text-to-SQL Agent Tool.

```text
[ Streamlit UI ] ──> [ FastAPI Backend ] ──> [ LangGraph Agent Controller ]
                                                    ├──> [ Qdrant (RAG) ]
                                                    └──> [ SQLite (SQL DB) ]


enterprise_ai_assistant/
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── steps.md
├── data/
│   └── sample_data.txt
├── src/
│   ├── config.py
│   ├── core/
│   │   ├── agent_controller.py
│   │   └── prompts.py
│   ├── modules/
│   │   ├── rag_pipeline.py
│   │   ├── rag_tool.py
│   │   └── sql_engine.py
│   ├── api/
│   │   └── main.py
│   └── evaluation/
│       └── evaluate_rag.py
└── frontend/
    └── app.py


#docker-compose up --build
Access the services:

Streamlit Frontend: http://localhost:8501

FastAPI Swagger Docs: http://localhost:8000/docs

Qdrant Dashboard: http://localhost:6333/dashboard