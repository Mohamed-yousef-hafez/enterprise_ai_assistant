# سكريبت مبسط لاختبار استجابة الـ RAG مقارنة بالإجابة المتوقعة
from src.modules.rag_pipeline import hybrid_search

def evaluate_retrieval_pipeline():
    test_queries = [
        {"query": "ما هي سياسة الإجازات؟", "expected_keyword": "إجازة"}
    ]
    
    print("Starting RAG Evaluation...")
    for item in test_queries:
        results = hybrid_search(item["query"], limit=1)
        if results and item["expected_keyword"] in results[0]["content"]:
            print(f"✅ PASSED for query: '{item['query']}'")
        else:
            print(f"❌ FAILED for query: '{item['query']}'")

if __name__ == "__main__":
    evaluate_retrieval_pipeline()