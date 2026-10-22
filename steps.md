---

### 3. ملف `steps.md`
هذا الملف يلخص خطة العمل ومراحل تطوير المشروع (Sprint-by-Sprint Development Roadmap)، وهو مفيد جداً للمتابعة وتتبع الإنجاز داخل الفريق.

```markdown
# 📋 Project Development Roadmap (Steps Brief)

This document outlines the step-by-step implementation phases for the Enterprise RAG & Agent system.

---

## 🟢 Phase 1: Environment Setup & Advanced RAG (Sprint 1)
- [x] **Step 1.1:** Setup Qdrant vector database container via Docker.
- [x] **Step 1.2:** Configure Python environment and `requirements.txt`.
- [x] **Step 1.3:** Build document chunking, embedding generation, and Qdrant ingestion (`rag_pipeline.py`).
- [x] **Step 1.4:** Implement Hybrid search retrieval mechanisms.

---

## 🟡 Phase 2: Structured Data & Agent Tools (Sprint 2)
- [x] **Step 2.1:** Initialize SQLite relational database with sample enterprise data (`sql_tool.py`).
- [x] **Step 2.2:** Build secure Text-to-SQL tool with strict `SELECT` query validation.
- [x] **Step 2.3:** Wrap RAG and SQL functions into LangChain/LangGraph tools (`rag_pipeline.py`).

---

## 🟠 Phase 3: LangGraph Controller & Core Logic (Sprint 3)
- [x] **Step 3.1:** Define system prompts and configurations (`config.py` & `prompts.py`).
- [x] **Step 3.2:** Build ReAct Agent loop using LangGraph (`agent_controller.py`) for dynamic tool routing.

---

## 🔵 Phase 4: API, Frontend & Containerization (Sprint 4)
- [x] **Step 4.1:** Develop FastAPI backend endpoints with asynchronous support (`main.py`).
- [x] **Step 4.2:** Build interactive Streamlit chat interface (`frontend/app.py`).
- [x] **Step 4.3:** Setup evaluation script for retrieval validation (`evaluate_rag.py`).
- [x] **Step 4.4:** Configure `Dockerfile` and `docker-compose.yml` for seamless multi-container deployment.