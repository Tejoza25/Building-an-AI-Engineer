# 📅 Day 43 — Conversational RAG with Query Contextualization

**Date:** Day 43 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 7 — Production RAG
**Goal:** Implement multi-turn conversational retrieval by re-writing context-dependent follow-up queries into standalone search inputs using LangChain primitives.

---

## 🎯 Architectural Mechanics

```text
[ User Follow-Up Query + Chat History ]
                 │
                 ▼
[ Query Contextualization Prompt + LLM ] ──> Formulates Standalone Query
                 │
                 ▼
     [ Vector Store Retriever ]          ──> Fetches Relevant Document Chunks
                 │
                 ▼
   [ Synthesis Prompt + LLM ]            ──> Context-grounded Answer with History

🛠️ Core Components Used

1. create_history_aware_retriever: A sub-chain that reformulates incoming questions into standalone search prompts when prior history exists.

2. create_stuff_documents_chain: Feeds retrieved documents directly into an LLM answer prompt.

3. create_retrieval_chain: Combines the history-aware retriever and document synthesis chain into an end-to-end runnable.