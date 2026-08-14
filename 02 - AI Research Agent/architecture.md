# 🏗️ AI Research Agent — Architecture

## System Overview

The AI Research Agent is a multi-stage research pipeline that combines web retrieval, content extraction, LLM summarization, synthesis, and Markdown persistence.

```text
                         USER
                          │
                          ▼
                  Research Topic
                          │
                          ▼
                 ┌────────────────┐
                 │ DuckDuckGo     │
                 │ Web Search     │
                 └───────┬────────┘
                         │
                         ▼
                    Top 3 URLs
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          Source 1    Source 2    Source 3
             │           │           │
             ▼           ▼           ▼
          Requests    Requests    Requests
             │           │           │
             ▼           ▼           ▼
       BeautifulSoup BeautifulSoup BeautifulSoup
             │           │           │
             ▼           ▼           ▼
        Source Text Source Text Source Text
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
                    Final LLM
                    Synthesis
                         │
                         ▼
                 Research Report
                         │
                         ▼
                  Markdown File
                         │
                         ▼
                     reports/