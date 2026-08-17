# 📅 Day 30 — Conversation Memory in LangChain

**Date:** Day 30 of 90
**Module:** 3 — LangChain & RAG Foundations
**Week:** 5 — LangChain Basics
**Goal:** Build a LangChain chatbot that maintains conversation history across multiple turns.

---

## 🎯 What I Learned Today

### The Problem: LLMs Have No Memory

Every call to an LLM is **stateless**. The model doesn't remember previous messages in a conversation. If you call `llm.invoke("Hi, I'm Tejoza")` and then `llm.invoke("What's my name?")`, it won't know your name.

### The Solution: Pass History Manually (or Use Memory Classes)

To make a chatbot that "remembers", you need to send the **previous messages** along with each new message. LangChain provides memory abstractions to handle this for you.

### Chat Models vs. LLMs

| Type | What | Use |
|------|------|-----|
| **LLMs** | Take a string, return a string | Simple completions, legacy code |
| **Chat Models** | Take a list of messages, return a message | Modern chatbots, conversational apps |

For Day 30, we use **Chat Models** because they support system/user/assistant message roles — exactly what multi-turn conversations need.

### Message Types

- **SystemMessage** — sets the AI's behavior (e.g. "You are a helpful tutor")
- **HumanMessage** — what the user says
- **AIMessage** — what the AI responds with

### Modern Memory: RunnableWithMessageHistory

In LangChain v1.x, the old `ConversationBufferMemory` class is deprecated. The modern way is:

1. Define a **get_session_history** function that returns a `ChatMessageHistory` for each session
2. Wrap your chain in `RunnableWithMessageHistory`
3. Pass a `session_id` so different users have separate conversations

```python
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
