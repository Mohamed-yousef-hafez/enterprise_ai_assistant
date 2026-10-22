import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models

load_dotenv()

# 1. إعداد الاتصال بـ Qdrant المحلّي عبر Docker
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "enterprise_knowledge_base"

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# 2. إعداد نموذج الـ Embeddings من OpenAI
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")


def init_vector_collection():
    """التحقق من وجود الكولكشن في Qdrant أو إنشاؤه إذا لم يكن موجوداً"""
    collections = client.get_collections().collections
    exists = any(col.name == COLLECTION_NAME for col in collections)
    
    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=1536,  دحجم الـ embedding الخاص بنموذج text-embedding-3-small
                distance=models.Distance.COSINE
            ),
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already exists.")


def ingest_documents(file_path: str):
    """تقسيم المستندات وتخزينها في Qdrant"""
    if not os.path.exists(file_path):
        print(f"File {file_path} not found. Please create a sample text file first.")
        return

    # قراءة وتقسيم الملف
    loader = TextLoader(file_path, encoding="utf-8")
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(docs)
    
    # توليد وتخزين النقاط (Points) في Qdrant
    points = []
    for idx, chunk in enumerate(chunks):
        vector = embeddings.embed_query(chunk.page_content)
        points.append(
            models.PointStruct(
                id=idx,
                vector=vector,
                payload={
                    "page_content": chunk.page_content,
                    "source": file_path
                }
            )
        )
    
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print(f"Successfully ingested {len(chunks)} chunks into Qdrant!")


def hybrid_search(query: str, limit: int = 3):
    """دالة الاسترجاع (Retrieval) - حالياً تعتمد على Vector Search، ويمكن توسيعها لدمج BM25"""
    query_vector = embeddings.embed_query(query)
    
    search_results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit
    )
    
    results = []
    for scored_point in search_results:
        results.append({
            "content": scored_point.payload.get("page_content"),
            "score": scored_point.score
        })
    return results