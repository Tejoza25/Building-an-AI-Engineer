📅 Day 52 — Local Dense Embeddings & Persistent Chroma Indexing

Project: 04 - Hardened Financial & SEC Filing Copilot
Module: 3 — LangChain & RAG Foundations (Project 2 Milestone)
Week: 8 — Build & Ship
Goal: Convert table-preserved SEC filing chunks into 384-dimensional dense vectors using local Hugging Face embeddings, persist the index to disk with ChromaDB, and execute targeted metadata-filtered similarity queries.

🎯 Architectural Role of Vector Indexing

[ Day 51: Ingested Chunks + Metadata ]
                  │
                  ▼
  [ HuggingFaceEmbeddings ]
  (sentence-transformers/all-MiniLM-L6-v2)
  • Runs 100% locally on CPU (0 API cost)
  • 384-dimensional unit-normalized vectors
                  │
                  ▼
  [ Chroma Persistent Vector DB ]
  (data/chroma_financial_db/)
  • Embedded text + metadata written to disk
                  │
                  ▼
  [ Filtered Similarity Search ]
  • Filter: {"statement_type": "Income Statement"}
  • Returns exact table chunks for query matching

⚙️ Key Technical Components

Local Embeddings: sentence-transformers/all-MiniLM-L6-v2 provides lightweight, fast dense vectorization for financial text without calling external APIs.

Persistent Storage: Stored in data/chroma_financial_db/ so downstream LCEL chains (Day 53) and Streamlit (Day 54) can query the index instantly without re-embedding filings every run.

Metadata Filtering: Enforces exact searches so queries about income statements only search chunks tagged with statement_type == "Income Statement".