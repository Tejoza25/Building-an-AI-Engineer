# 📅 Day 48 — RAG Evaluation & Benchmarking Metrics

**Date:** Day 48 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 7 — Production RAG
**Goal:** Implement automated RAG evaluation metrics to programmatically benchmark retrieval relevance, faithfulness (groundedness), and answer accuracy.

---

## 🎯 The RAG Triad of Evaluation

```text
               ┌───────────────────────┐
               │      User Query       │
               └───────────┬───────────┘
                           │
             Context Relevance (Retrieval)
                           │
                           ▼
               ┌───────────────────────┐
               │   Retrieved Context   │
               └───────────┬───────────┘
                           │
             Faithfulness / Groundedness
                           │
                           ▼
               ┌───────────────────────┐
               │    Synthesized Answer │
               └───────────┬───────────┘
                           │
             Answer Relevance (Synthesis)
                           │
                           ▼
               ┌───────────────────────┐
               │     User Evaluation   │
               └───────────────────────┘

🛠️ Core Evaluation Metrics

1. Context Relevance: Evaluates whether the retriever fetched only information pertinent to the question, filtering out noise.

2. Faithfulness (Groundedness): Measures whether every claim in the generated answer can be mathematically derived from the retrieved context.

3. Answer Relevance: Determines if the final generated output directly addresses the original intent of the prompt.