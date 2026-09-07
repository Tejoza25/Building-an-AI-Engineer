# 📅 Day 39 — Vector Embeddings

**Date:** Day 39 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 6 — RAG Systems
**Goal:** Understand vector embeddings, map text into high-dimensional semantic vectors using `sentence-transformers`, and compute cosine similarity.

---

## 🎯 What I Learned Today

### 1. What Are Vector Embeddings?
Vector embeddings are dense numerical arrays (e.g., 384 or 1536 floating-point numbers) that capture the underlying semantic meaning of text. 

- Words or sentences with similar contextual meanings map close to one another in vector space.
- Unlike keyword matching, embeddings capture synonyms, context, and intent (e.g., `"automobile"` and `"car"` yield a high similarity score).

---

### 2. Distance & Similarity Metrics

| Metric | Formula / Concept | Usage Context |
| :--- | :--- | :--- |
| **Cosine Similarity** | Normalized dot product: $\cos(\theta) = \frac{A \cdot B}{\Vert{}A\Vert{} \Vert{}B\Vert{}}$ | Measures angle/direction regardless of vector magnitude (Scale: -1 to 1) |
| **Dot Product** | Sum of element-wise products | Fast; identical to cosine similarity when vectors are unit-normalized |
| **Euclidean Distance ($L_2$)** | Straight-line distance between two points | Measures absolute distance; sensitive to vector magnitude |

---

### 3. Open-Source vs. Proprietary Embeddings

| Feature | `sentence-transformers/all-MiniLM-L6-v2` | OpenAI `text-embedding-3-small` |
| :--- | :--- | :--- |
| **Hosting** | Local (Runs on CPU/GPU) | Cloud API |
| **Cost** | 100% Free | Pay-per-token API cost |
| **Dimensions** | 384 | 1536 (default) |
| **Privacy** | High (Data never leaves machine) | Data sent over external network |

---

## 🏗️ Ingestion Pipeline Flow

```text
[ Document Loaders ] (Day 37)
         │
         ▼
[ Text Splitters ] (Day 38)
         │
         ▼
[ Embedding Generation ] (Day 39) ──> [ Vector Stores: FAISS/Chroma ] (Day 40)