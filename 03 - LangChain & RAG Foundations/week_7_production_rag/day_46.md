# 📅 Day 46 — Production Prompt Engineering & Factual Grounding

**Date:** Day 46 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 7 — Production RAG
**Goal:** Implement battle-tested prompt engineering patterns in LCEL to prevent hallucinations, enforce explicit context-bound rejection, and maintain strict factual integrity.

---

## 🎯 Production Prompt Anatomy

```text
┌─────────────────────────────────────────────────────────────────┐
│ 1. Role & Identity Boundary (Objective persona)                │
├─────────────────────────────────────────────────────────────────┤
│ 2. Negative Constraints (No prior parametric knowledge leakage) │
├─────────────────────────────────────────────────────────────────┤
│ 3. Explicit Refusal Anchor ("I do not have sufficient info...") │
├─────────────────────────────────────────────────────────────────┤
│ 4. Structured Context Envelope ({context})                      │
├─────────────────────────────────────────────────────────────────┤
│ 5. Specific User Query ({question})                             │
└─────────────────────────────────────────────────────────────────┘

🛠️ Key Guardrail Techniques

1. Explicit Negative Constraints: Explicitly instructing the LLM to ignore pre-trained internal knowledge and rely solely on the presented context string.

2. Deterministic Rejection Trigger: Defining the exact fallback phrase (e.g., "I do not possess sufficient information to answer this based on the provided documents.") when the retriever cannot satisfy the query.

3. Purity Isolation: Stripping external bias and ensuring context blocks are cleanly delineated with standard boundary tags.