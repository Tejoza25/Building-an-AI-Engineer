# 📅 Day 29 — LangChain Fundamentals

**Date:** Day 29 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 5 — LangChain Basics
**Goal:** Understand what LangChain is, why it exists, and build my first LangChain-powered LLM chain using LCEL.

---

## 🎯 What I Learned Today

### What is LangChain?

LangChain is an open-source framework for building applications powered by Large Language Models (LLMs)[cite: 3]. It provides:

- **Standard interfaces** for connecting to LLMs (OpenAI, Anthropic, OpenRouter, etc.)[cite: 3]
- **Chains** to combine multiple LLM calls and processing steps[cite: 3]
- **Prompt Templates** for reusable, parameterized prompts[cite: 3]
- **Output Parsers** to extract structured data from LLM responses[cite: 3]
- **Memory** to maintain conversation context[cite: 3]
- **Tools and Agents** for autonomous AI behavior[cite: 3]
- **Vector stores and retrievers** for RAG applications[cite: 3]

---

### Why Use LangChain Instead of Raw OpenAI SDK?

| Aspect | Raw OpenAI SDK | LangChain |
| :--- | :--- | :--- |
| **Prompt construction** | Manual string formatting[cite: 3] | PromptTemplate objects[cite: 3] |
| **Chaining calls** | Manual code blocks[cite: 3] | Composable LCEL chains (`\|`)[cite: 3] |
| **Memory** | Manual message list management[cite: 3] | Built-in memory & history modules[cite: 3] |
| **Tool calling** | Manual function definitions[cite: 3] | Decorator-based tool creation[cite: 3] |
| **Output parsing** | Manual JSON parsing[cite: 3] | OutputParser classes[cite: 3] |
| **Multi-LLM support** | Rewrite code per provider[cite: 3] | Swap providers with one line[cite: 3] |
| **Vector databases** | Build from scratch[cite: 3] | Pre-built integrations[cite: 3] |

---

### LangChain Core Concepts

1. **LLMs and Chat Models** — Unified interfaces for model APIs[cite: 3]
2. **Prompt Templates** — Parameterized, reusable prompt construction[cite: 3]
3. **Chains (LCEL)** — Composable sequences of calls via the pipe operator (`|`)[cite: 3]
4. **Output Parsers** — Transform raw model output into structured, typed data[cite: 3]
5. **Memory** — Persist conversation state across turns[cite: 3]
6. **Retrievers** — Fetch relevant context from vector stores[cite: 3]
7. **Agents** — Dynamic reasoning systems that determine execution paths[cite: 3, 7]
8. **Tools** — Functions the agent can invoke to interact with the real world[cite: 3, 7]

---

## 🛠️ Installation Journey — Issues & Fixes

1. **`ModuleNotFoundError: No module named 'langchain.chains'`**[cite: 3]
   - *Cause:* Modern LangChain deprecated legacy `LLMChain` in favor of LangChain Expression Language (LCEL)[cite: 3].
   - *Fix:* Replaced legacy chain syntax with modern LCEL: `chain = prompt | llm | parser`[cite: 3].

2. **`ModuleNotFoundError: No module named 'langchain.prompts'`**[cite: 3]
   - *Cause:* Prompts were moved to core package imports[cite: 3].
   - *Fix:* Updated import to `from langchain_core.prompts import PromptTemplate`[cite: 3].

3. **`ModuleNotFoundError: No module named 'dotenv'`**[cite: 3]
   - *Cause:* `python-dotenv` was missing in the virtual environment[cite: 3].
   - *Fix:* Ran `python -m pip install python-dotenv`[cite: 3].

4. **`AuthenticationError: 401 - User not found`**[cite: 3]
   - *Cause:* `.env` contained a placeholder API key[cite: 3].
   - *Fix:* Added valid OpenRouter API key from https://openrouter.ai/keys[cite: 3].

5. **The `.env` Path Issue**[cite: 3]
   - *Cause:* `load_dotenv()` defaults to the working directory, missing the root file[cite: 3].
   - *Fix:* Loaded explicitly via `load_dotenv(dotenv_path="../.env")`[cite: 3].

---

## 💻 My First LangChain Chain (Modern LCEL)

I built a runnable chain that:
- Takes a topic parameter as input[cite: 3]
- Formats a research prompt via `PromptTemplate`[cite: 3]
- Queries an LLM via OpenRouter[cite: 3]
- Parses raw output into a clean string using `StrOutputParser`

```python
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv(dotenv_path="../.env")

# Initialize Chat Model via OpenRouter
llm = ChatOpenAI(
    base_url="[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="nvidia/nemotron-3-ultra-550b-a55b:free"
)

# Define reusable prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in 3 short bullet points."
)

# Modern LCEL Chain: Prompt -> LLM -> Output Parser
chain = prompt | llm | StrOutputParser()

# Invoke the chain
result = chain.invoke({"topic": "LangChain"})
print(result)