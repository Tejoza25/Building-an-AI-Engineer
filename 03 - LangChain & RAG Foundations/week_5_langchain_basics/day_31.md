# 📅 Day 31 — Output Parsers & Structured Data

**Date:** Day 31 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 5 — LangChain Basics
**Goal:** Build LangChain chains that return structured, typed data instead of free-form text.

---

## 🎯 What I Learned Today

### The Problem with Raw LLM Output

LLMs are trained to produce natural language. When you ask for JSON, you might get:
- A nicely formatted JSON
- JSON wrapped in markdown code blocks (```json ... ```)
- Almost-JSON with extra commentary
- A JSON-like string that fails to parse

This makes integrating LLMs into applications **fragile and unreliable**.

### The Solution: Output Parsers

Output parsers:
1. Define a **schema** (what the output should look like)
2. Inject schema instructions into the prompt
3. Parse the LLM's response to match the schema
4. Return a **typed** object (Pydantic) or a structured dict (JSON)

### Pydantic — Foundation of Modern Parsing

Pydantic is a Python library that uses type hints for data validation:

```python
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="Person's full name")
    age: int = Field(description="Person's age in years")
    skills: list[str] = Field(description="List of skills")
