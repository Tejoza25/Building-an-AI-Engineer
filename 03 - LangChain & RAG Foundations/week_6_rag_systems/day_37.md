# 📅 Day 37 — Document Loaders in LangChain

**Date:** Day 37 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 6 — RAG Systems
**Goal:** Parse real-world files (.txt, .md, .pdf, and directories) into standard LangChain Document objects.

---

## 🎯 What I Learned Today

### 1. The Universal Document Contract
All LangChain document loaders normalize diverse input formats into a single, consistent schema:
- **`page_content`**: The raw string content of the document segment.
- **`metadata`**: Key-value dictionary tracking provenance (file path, title, page numbers). Metadata is critical for Day 44 source citation and filtering queries.

---

### 2. Common Document Loaders

| Loader | Package Import | Primary Purpose |
| :--- | :--- | :--- |
| `TextLoader` | `langchain_community.document_loaders` | Plaintext files (`.txt`, `.log`) with explicit character encodings |
| `UnstructuredMarkdownLoader` / `TextLoader` | `langchain_community.document_loaders` | Markdown developer notes and project guides (`.md`) |
| `PyPDFLoader` | `langchain_community.document_loaders` | PDF documents with automatic page-by-page document splitting |
| `DirectoryLoader` | `langchain_community.document_loaders` | Batch file ingestion via glob patterns across entire project trees |

---

## 🏗️ Ingestion Pipeline Architecture

```text
[ File System: .txt, .md, .pdf ]
               │
               ▼
      [ Document Loader ]
  (TextLoader, PyPDFLoader)
               │
               ▼
 [ Standard Document Objects ] ──> [ Day 38: Text Splitters ]
 (page_content + metadata)