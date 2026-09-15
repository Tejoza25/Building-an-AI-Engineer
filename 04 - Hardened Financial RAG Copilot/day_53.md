# 📅 Day 53 — Conversational LCEL Chains & Dual-Track Provenance

**Project:** 04 - Hardened Financial & SEC Filing Copilot  
**Module:** 3 — LangChain & RAG Foundations (Project 2 Milestone)  
**Week:** 8 — Build & Ship  
**Goal:** Construct an enterprise conversational RAG pipeline using LCEL with query contextualization, dual-track provenance routing (`RunnableParallel`), prompt guardrails, and automated model failovers.

---

## 🎯 Pipeline Architecture

```text
User Question + Chat History
             │
             ▼
[ Contextualization Chain ] ──> Rewrites follow-up queries into standalone search terms
             │
             ▼
      [ Chroma Retriever ] ─────> Fetches top relevant table chunks from disk
             │
    ┌────────┴────────────────────────────────────────┐
    ▼                                                 ▼
[ Track A: Context Formatter ]             [ Track B: Source Provenance ]
Formats chunks into bracketed prompts      Passes raw Document objects untouched
[Source 1], preserving table boundaries    for UI audit verification
    │                                                 │
    ▼                                                 │
[ Guardrailed System Prompt ]                         │
Strictly forbids unstated arithmetic                  │
    │                                                 │
    ▼                                                 │
[ Resilient LLM Engine ]                              │
gpt-4o-mini + fallback routing                        │
    │                                                 │
    └────────────────────────┬────────────────────────┘
                             ▼
              Final Payload: { answer, sources }