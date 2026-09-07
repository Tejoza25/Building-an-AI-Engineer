# 📅 Day 41 — End-to-End Retrieval Chain (LCEL & RAG)

**Date:** Day 41 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 6 — RAG Systems
**Goal:** Connect a persistent vector retriever to an LLM via LangChain Expression Language (LCEL) to build a fully automated question-answering RAG pipeline.

---

## 🎯 What I Learned Today

### 1. Vector Store as a Retriever
A Vector Store stores vectors and performs raw distance queries. A **Retriever** wraps the store with the standard LangChain `Runnable` interface, allowing it to be piped directly into chains using `.as_retriever()`.

```python
retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 2}
)

🏗️ Ingestion to Generation Flow

Plaintext
[ Raw Data ] (Day 37)
     │
     ▼
[ Chunks ] (Day 38)
     │
     ▼
[ Embeddings ] (Day 39)
     │
     ▼
[ Vector Store (Chroma) ] (Day 40)
     │
     ▼
[ RAG Chain (Retriever + Prompt + LLM) ] (Day 41) ──> Final Grounded Answer