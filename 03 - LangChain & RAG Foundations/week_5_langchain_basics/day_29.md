📅 Day 29 — LangChain Fundamentals

**Date:** Day 29 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 5 — LangChain Basics
**Goal:** Understand what LangChain is, why it exists, and build my first LangChain-powered LLM chain.

---

## 🎯 What I Learned Today

### What is LangChain?

LangChain is an open-source framework for building applications powered by Large Language Models (LLMs). It provides:

- **Standard interfaces** for connecting to LLMs (OpenAI, Anthropic, OpenRouter, etc.)
- **Chains** to combine multiple LLM calls and processing steps
- **Prompt Templates** for reusable, parameterized prompts
- **Output Parsers** to extract structured data from LLM responses
- **Memory** to maintain conversation context
- **Tools and Agents** for autonomous AI behavior
- **Vector stores and retrievers** for RAG applications

### Why Use LangChain Instead of Raw OpenAI SDK?

| Aspect | Raw OpenAI SDK | LangChain |
|--------|----------------|-----------|
| Prompt construction | Manual string formatting | PromptTemplate objects |
| Chaining calls | Manual code blocks | Composable chains |
| Memory | Manual message list management | Built-in memory modules |
| Tool calling | Manual function definitions | Decorator-based tool creation |
| Output parsing | Manual JSON parsing | OutputParser classes |
| Multi-LLM support | Rewrite code per provider | Swap providers with one line |
| Vector databases | Build from scratch | Pre-built integrations |

### LangChain Core Concepts

1. **LLMs and Chat Models** — wrappers around model APIs
2. **Prompt Templates** — parameterized, reusable prompts
3. **Chains** — sequences of calls to LLMs or other utilities
4. **Output Parsers** — extract structured data from responses
5. **Memory** — persist state between chain calls
6. **Retrievers** — fetch relevant documents from vector stores
7. **Agents** — let LLMs decide which tools to use
8. **Tools** — functions the agent can invoke

### My First LangChain Chain

### 🛠️ Installation Journey — What It Took to Get Running

I hit these issues in order and how I fixed them:

1. **`ModuleNotFoundError: No module named 'langchain.chains'`**
   - Cause: I had LangChain v1.3 installed, where `LLMChain` was removed
   - Fix: Updated code to use LCEL syntax: `chain = prompt | llm | parser`

2. **`ModuleNotFoundError: No module named 'langchain.prompts'`**
   - Cause: In v1.3, this was moved to `langchain_core.prompts`
   - Fix: Changed import to `from langchain_core.prompts import PromptTemplate`

3. **`ModuleNotFoundError: No module named 'dotenv'`**
   - Cause: `python-dotenv` wasn't installed in my venv
   - Fix: Ran `python -m pip install python-dotenv`

4. **`AuthenticationError: 401 - User not found`**
   - Cause: My .env had a placeholder instead of the real OpenRouter key
   - Fix: Updated .env with the real key from https://openrouter.ai/keys

5. **The `.env` path issue**
   - Cause: `load_dotenv()` looks for `.env` in the current directory, but my `.env` was one folder up
   - Fix: Used `load_dotenv(dotenv_path="../.env")` to specify the path

### ✅ Key Lessons Learned

- Always use **`python -m pip install`** to install to the right Python
- Use **virtual environments** to isolate dependencies
- Use **LCEL syntax** (the `|` operator) for modern LangChain code
- Always use **the path parameter** in `load_dotenv()` for reliable env loading
- Check **LangChain version** before writing code — the API changes between major versions

---


I built a chain that:
- Takes a topic as input
- Uses a PromptTemplate to construct a research prompt
- Sends it to an LLM via OpenRouter
- Returns the generated summary

```python
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="nvidia/nemotron-3-ultra-550b-a55b:free"
)

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Explain {topic} in 3 short bullet points."
)

chain = LLMChain(llm=llm, prompt=prompt)

result = chain.run("LangChain")
print(result)