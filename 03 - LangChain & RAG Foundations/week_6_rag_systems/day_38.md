# 📅 Day 38 — Text Splitters & Chunking Strategies

**Date:** Day 38 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 6 — RAG Systems
**Goal:** Master document chunking mechanics, examine split boundaries, and maintain semantic integrity using `RecursiveCharacterTextSplitter`.

---

## 🎯 Core Concepts

### 1. Why Chunking is Critical
- **Context Windows:** Embedding models and LLMs have maximum input limits.
- **Retrieval Precision:** Searching over 5,000-word documents yields diluted, broad vectors. Searching over 300-word chunks isolates precise facts.
- **Preventing Lost-in-the-Middle:** Tightly scoped context helps LLMs locate facts without attention degradation.

---

### 2. Chunk Size vs. Chunk Overlap

| Parameter | Function | Production Guideline |
| :--- | :--- | :--- |
| `chunk_size` | Maximum character/token limit per slice | 500–1000 characters for general QA |
| `chunk_overlap` | Duplicated text boundary between adjacent chunks | 10–20% of `chunk_size` (e.g., 50–150 characters) |

> **Why Overlap Matters:** If an answer spans across two sentences cut at character 500, a non-overlapping split slices the thought in half. Overlap ensures boundary context appears completely in at least one chunk.

---

### 3. Splitter Types

- **`CharacterTextSplitter`**: Naive split strictly on a single separator (e.g., `"\n\n"`). Risky if paragraphs are excessively long.
- **`RecursiveCharacterTextSplitter`**: The industry standard default. Recursively tries separators in descending order:
  1. `"\n\n"` (Paragraphs)
  2. `"\n"` (Line breaks)
  3. `" "` (Spaces / words)
  4. `""` (Individual characters as fallback)
- **`MarkdownHeaderTextSplitter`**: Splits structured documentation according to header levels (`#`, `##`, `###`), preserving hierarchical context in metadata.

---

## 🏗️ Pipeline Ingestion Progress

```text
[ Raw Files (.txt, .md) ] (Day 37)
           │
           ▼
[ Standard Documents ] (Day 37)
           │
           ▼
[ Recursive Chunking with Overlap ] (Day 38)
           │
           ▼
[ Semantic Embeddings ] (Day 39)