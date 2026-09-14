# 📅 Day 50 — System Architecture & Design Specifications

**Project:** 04 - Hardened Financial & SEC Filing Copilot
**Module:** 3 — LangChain & RAG Foundations (Project 2 Milestone)
**Week:** 8 — Build & Ship
**Goal:** Scope out system architecture, tabular markdown ingestion strategies, schema metadata tags, prompt guardrails, and environment configuration for an enterprise financial knowledge assistant.

---

## 🎯 System Architecture Diagram

```text
====================================================================================================
           END-TO-END QUERY-TO-RESPONSE PIPELINE: HARDENED FINANCIAL RAG COPILOT
====================================================================================================

[ USER INTERACTION ]
  │
  │  User types query into Streamlit UI:
  │  "What was NVIDIA's data center revenue in FY2025, and how did it compare to FY2024?"
  │
  ▼
[ STAGE 1: CONVERSATIONAL CONTEXTUALIZATION ]
  │
  ├── Inputs: Raw Question + Chat History (Prior Turns)
  │
  ├── Contextualizer Prompt & LLM:
  │   └── Resolves ambiguous pronouns, relative dates, and ticker references
  │
  └── Output: Standalone Search Query
      "NVIDIA FY2025 data center revenue vs FY2024 data center revenue"
  │
  ▼
[ STAGE 2: TARGETED METADATA EXTRACTION & FILTERING ]
  │
  ├── Structured Rule / Query Classifier:
  │   ├── Extracts target ticker: "NVDA"
  │   ├── Identifies target periods: [2024, 2025]
  │   └── Identifies target sections: "Segment Results" / "Revenue Highlights"
  │
  └── Generates Chroma filter dictionary:
      {"$and": [{"ticker": "NVDA"}, {"fiscal_year": {"$in": [2024, 2025]}}]}
  │
  ▼
[ STAGE 3: VECTOR RETRIEVAL & PROVENANCE FETCHING ]
  │
  ├── Hugging Face Embeddings (`all-MiniLM-L6-v2`):
  │   └── Converts standalone query into a 384-dimensional dense vector
  │
  ├── Chroma Vector Database:
  │   └── Executes Approximate Nearest Neighbor (ANN) search over filtered subset
  │
  └── Output: Top-K Grounded Document Chunks (K=3)
      └── Intact tabular rows + complete metadata:
          [Chunk 1]: NVDA FY25 Data Center Revenue table ($47.5B, etc.) | Source: nvda_fy24_fy25_10k.md
          [Chunk 2]: NVDA FY24 Data Center Revenue segment | Source: nvda_fy24_fy25_10k.md
  │
  ▼
[ STAGE 4: DUAL-TRACK LCEL EXECUTION (RunnableParallel) ]
  │
  ├────────────────────────────────────────┬────────────────────────────────────────┐
  │ Track A: Context Serialization         │ Track B: Source Provenance Isolation   │
  │                                        │                                        │
  │ • Retains Markdown table boundaries    │ • Isolates metadata keys:              │
  │ • Injects explicit bracketed tags:     │   - source_file                        │
  │   [Source 1: nvda_fy24_fy25_10k.md]   │   - fiscal_year                        │
  │ • Serializes into prompt text          │   - statement_type                     │
  │                                        │ • Holds untouched for UI audit         │
  └────────────────────────────────────────┴────────────────────────────────────────┘
  │
  ▼
[ STAGE 5: FACTUAL SYNTHESIS & GUARDRAIL PROMPT ]
  │
  ├── Prompt Template:
  │   ├── Instruction: Answer using ONLY the provided Markdown context
  │   ├── Arithmetic Guardrail: Do NOT calculate unstated ratios; quote exact figures
  │   ├── Refusal Guardrail: If metrics are missing, output "Data not disclosed"
  │   └── Citation Tagging: Attach bracketed tags ([Source 1]) to every figure
  │
  └── Primary LLM Inference (`gpt-4o-mini` via OpenAI / OpenRouter fallback):
      └── Processes prompt + serialized tabular context
  │
  ▼
[ STAGE 6: STREAMING DELIVERY & AUDIT PRESENTATION ]
  │
  ├── Streamlit Output Generator:
  │   ├── Streams tokens in real time (immediate Time-to-First-Token)
  │   └── Prints synthesized answer:
  │       "In FY2025, NVIDIA's Data Center revenue was $115,180 million [Source 1],
  │        compared to $47,525 million in FY2024 [Source 2]..."
  │
  └── UI Provenance Inspector:
      └── Renders collapsible sidebar with raw chunk text, tables, and file metadata

```

---

## ⚖️ Engineering Challenges & Mitigations

| **Challenge**                | **Why Naive RAG Fails**                                                                                      | **Hardened Solution (Project 4)**                                                                                                             |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tabular Financial Data**   | Standard character splitters slice text arbitrarily, disconnecting numbers from row labels and column dates. | Structural Markdown splitting preserving balance sheet and revenue tables intact within single chunk contexts.                                |
| **Arithmetic Hallucination** | LLMs invent arbitrary decimals and inaccurate percentage calculations.                                       | Strict factual prompt guardrails: model quotes audited figures and states "Data not disclosed" rather than extrapolating unstated arithmetic. |
| **Pronoun References**       | Multi-turn queries fail on pronouns (*"How much did it grow?"*).                                             | History-aware query contextualizer rewrites references into standalone search queries before vector lookup.                                   |
| **Audit Provenance**         | Black-box output is unacceptable in compliance and audit scenarios.                                          | Dual-track LCEL (`RunnableParallel`) passes document provenance directly to the UI inspector for side-by-side verification.                   |
| **Endpoint Outages**         | API rate limits (429) or cloud errors (502) crash brittle pipelines.                                         | LCEL `.with_fallbacks()` automatically routes requests to secondary models.                                                                   |

---

## 📋 Metadata Specification Schema

Every indexed chunk must conform to this schema:

* `ticker` (str): Stock ticker symbol (e.g., `"NVDA"`).
* `fiscal_year` (int): Target filing year (e.g., `2024`, `2025`).
* `fiscal_period` (str): Reporting interval (`"FY"`, `"Q1"`, `"Q2"`, `"Q3"`).
* `statement_type` (str): Category (e.g., `"Income Statement"`, `"Data Center"`, `"Risk Factors"`).
* `source_file` (str): Origin file name (e.g., `"nvda_fy24_fy25_10k.md"`).

---

## 📁 Repository Directory Layout

```text
Building-an-AI-Engineer/
├── 01 - AI Engineering Foundations/
├── 02 - AI Research Agent/
├── 03 - LangChain & RAG Foundations/
└── 04 - Hardened Financial RAG Copilot/
    ├── data/
    │   ├── raw/
    │   │   └── nvda_fy24_fy25_10k.md
    │   └── chroma_financial_db/       # Local persistent vector store (gitignored)
    ├── src/
    │   ├── __init__.py
    │   ├── config.py                  # Environment, paths, and model configurations
    │   ├── ingestion.py               # Table-aware parser & metadata tagging (Day 51)
    │   └── chains.py                  # Dual-branch conversational LCEL chains (Day 53)
    ├── app.py                         # Streamlit interactive UI (Days 54–55)
    ├── requirements.txt               # Pinned project dependencies
    ├── README.md                      # Technical recruiter portfolio overview
    └── day_50.md                      # Day 50 technical specification
```
