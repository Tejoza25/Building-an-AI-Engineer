# 📅 Day 51 — Automated Ingestion & Tabular Markdown Processing

**Project:** 04 - Hardened Financial & SEC Filing Copilot
**Module:** 3 — LangChain & RAG Foundations (Project 2 Milestone)
**Week:** 8 — Build & Ship
**Goal:** Implement a structure-aware ingestion pipeline that preserves markdown tables, extracts rich financial metadata, and chunks SEC filings without severing numerical context.

---

## 🎯 The Core Financial Ingestion Problem

In standard text pipelines, splitters rely strictly on character counts or newlines. When applied to SEC filings containing balance sheets or revenue tables:

1. **Header Decoupling:** Rows get separated from their date columns (e.g., `$115,180M` separated from `FY2025`).
2. **Context Loss:** LLMs cannot interpret bare numbers without their categorical parent headers.
3. **Retrieval Degradation:** Embeddings generated from sliced tabular rows fail similarity matching.

---

## 🏗️ Structure-Aware Ingestion Pipeline

```text
[ Raw SEC Filing: nvda_fy24_fy25_10k.md ]
                   │
                   ▼
     [ Section Header Parsing (##) ]
                   │
                   ▼
     [ Table Boundary Detection ] ──────> Keeps tables as atomic units
                   │
                   ▼
    [ Rich Metadata Tag Injection ] ─────> Adds: ticker, year, statement_type
                   │
                   ▼
    [ Standard LangChain Documents ] ────> Ready for Vector Indexing (Day 52)
```

---

## 📋 Audited Metadata Schema

Every generated chunk contains verified metadata keys:

* `ticker`: Stock symbol (e.g., `NVDA`)
* `fiscal_year`: Int identifier (`2024`, `2025`)
* `fiscal_period`: Target interval (`FY`, `Q1`, `Q2`, `Q3`)
* `statement_type`: Financial section (`Income Statement`, `Data Center`, `Free Cash Flow`, `Risk Factors`)
* `source_file`: Target filing origin filename
