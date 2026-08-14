# 🤖 AI Research Agent

> **Module 2 of 2** in my AI Engineering learning portfolio.
> Tracks Days 22–28 — building and shipping a complete multi-source research pipeline.

A practical AI research pipeline that searches the web, extracts information, summarizes multiple sources with an LLM, and produces a structured Markdown research report.

Built as **Project 1** of the AI Engineering Foundations journey.

---

## 🔗 Module Map

This is **Module 2** of a two-module portfolio:

| Module | Path | Days | Status |
|--------|------|------|--------|
| 1 — AI Engineering Foundations | [`01 - AI Engineering Foundations/`](../01%20-%20AI%20Engineering%20Foundations/) | 1–21 | ✅ |
| 2 — AI Research Agent | [`02 - AI Research Agent/`](../02%20-%20AI%20Research%20Agent/) | 22–28 | 🚧 In progress |

---

## 🎯 What I Built

I built a research agent that transforms a simple research question into a structured research report.

The system combines:

* 🔎 Web search
* 🌐 Web scraping
* 🧹 HTML content extraction
* 🧠 LLM-powered summarization
* 🔗 Multi-source synthesis
* 📝 Markdown report generation
* 🛡️ Error handling
* 🔐 Environment-based API key management

The project was developed incrementally to understand how individual AI engineering components combine into a practical application.

---

# 🧠 System Architecture

```text
                         USER
                          │
                          ▼
                  ┌───────────────┐
                  │ Research Topic│
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ Web Search    │
                  │   DuckDuckGo  │
                  └───────┬───────┘
                          │
                          ▼
                    Top 3 Sources
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
          Source 1    Source 2    Source 3
              │           │           │
              ▼           ▼           ▼
          HTTP/BS4    HTTP/BS4    HTTP/BS4
              │           │           │
              ▼           ▼           ▼
          Web Text    Web Text    Web Text
              │           │           │
              ▼           ▼           ▼
             LLM         LLM         LLM
              │           │           │
              ▼           ▼           ▼
          Summary     Summary     Summary
              └───────────┼───────────┘
                          │
                          ▼
                  Combined Summaries
                          │
                          ▼
                  ┌───────────────┐
                  │ Final LLM     │
                  │ Synthesis     │
                  └───────┬───────┘
                          │
                          ▼
                 Research Report
                          │
                          ▼
                    Markdown File
                          │
                          ▼
                       reports/
