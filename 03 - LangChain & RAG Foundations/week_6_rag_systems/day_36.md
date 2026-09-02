# 📅 Day 36 — What is Retrieval-Augmented Generation (RAG)?

**Date:** Day 36 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 6 — RAG Systems
**Goal:** Understand the architectural fundamentals of RAG, why external context prevents LLM hallucination, and build a foundational retrieval-generation flow.

---

## 🎯 What I Learned Today

### The Parametric Problem

LLMs store their knowledge inside neural network weights (**parametric memory**). This introduces three critical failure points for enterprise applications:
1. **Knowledge Cutoffs:** The model cannot answer questions about events or data created after training.
2. **Hallucination:** Under uncertainty, models generate plausible-sounding falsehoods rather than admitting ignorance.
3. **Private Data Inaccessibility:** Base models have never seen your private notes, proprietary codebases, or internal documentation.

### The Solution: Non-Parametric Grounding (RAG)

Retrieval-Augmented Generation decouples **reasoning** from **knowledge storage**:
- **Parametric Engine (LLM):** Acts purely as an inference, synthesis, and language generation engine.
- **Non-Parametric Store (External Knowledge):** Stores your private, up-to-date facts (vector stores, databases, documentation).

At query time, the system fetches relevant facts from storage and feeds them into the model's immediate context window.

---

## ⚖️ RAG vs. Fine-Tuning

| Dimension | Retrieval-Augmented Generation (RAG) | Fine-Tuning |
| :--- | :--- | :--- |
| **Primary Purpose** | Information retrieval & factual accuracy | Style, behavior, formatting, domain vocabulary |
| **Data Freshness** | Real-time (instant updates via database) | Static (requires continuous retraining) |
| **Hallucination Rate** | Low (strictly grounded in retrieved text) | Moderate to High |
| **Auditability** | High (exact document chunks are verifiable) | Low (black-box weight updates) |
| **Compute Cost** | Low setup cost; standard inference queries | High training compute & GPU resources |

---

## 🏗️ The Three Core Phases of RAG

```text
1. INGESTION:
   [Raw Files] ──> [Document Loaders] ──> [Text Chunker] ──> [Embedding Model] ──> [Vector DB]

2. RETRIEVAL:
   [User Query] ──> [Query Embedding] ──> [Similarity Search] ──> [Top-K Chunks]

3. SYNTHESIS:
   [Top-K Chunks] + [User Query] ──> [Augmented Prompt] ──> [LLM] ──> [Final Answer]