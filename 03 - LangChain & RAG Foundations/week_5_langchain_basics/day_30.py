"""
Day 30 - Conversation Memory in LangChain

Goal: Build a multi-turn chatbot that remembers conversation history.

This script demonstrates:
- Chat Models (ChatOpenAI) instead of raw LLMs
- Message types: SystemMessage, HumanMessage, AIMessage
- RunnableWithMessageHistory for modern memory management
- Session-based conversation isolation
- Multi-turn dialogue with context retention

Author: Tejoz
"""

import os
import sys
 
from dotenv import load_dotenv
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
TEMPERATURE = 0.5
TIMEOUT = 30
DEFAULT_SESSION_ID = "default_user"


# ============================================================
# ENVIRONMENT
# ============================================================

# Load .env from the module folder (one level up from this script)
from pathlib import Path

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ OPENROUTER_API_KEY is not set.")
    print(f"Looking for .env at: {env_path}")
    print(f"File exists: {env_path.exists()}")
    sys.exit(1)


# ============================================================
# LLM SETUP
# ============================================================

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    model=MODEL,
    temperature=TEMPERATURE,
    timeout=TIMEOUT,
)


# ============================================================
# PROMPT WITH HISTORY PLACEHOLDER
# ============================================================

# MessagesPlaceholder is where the previous conversation history will be inserted
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a friendly and helpful AI assistant. "
            "You remember things the user tells you during the conversation."
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)


# ============================================================
# CHAIN SETUP (LCEL — Modern LangChain Syntax)
# ============================================================

chain = prompt | llm


# ============================================================
# MEMORY STORE
# ============================================================

# In-memory store for chat histories, keyed by session_id
# In production, replace with a persistent store (Redis, DB, etc.)
store = {}


def get_session_history(session_id: str) -> ChatMessageHistory:
    """Get or create a chat history for a session."""
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# Wrap the chain with history-aware runnable
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


# ============================================================
# DEMO
# ============================================================

def chat_loop():
    """Run an interactive multi-turn chat session."""

    print("=" * 60)
    print("🦜 LangChain Day 30 — Chat with Memory")
    print("=" * 60)
    print()
    print("This chatbot remembers your conversation!")
    print("Type your message and press Enter. Type 'exit' or 'quit' to stop.")
    print()

    session_id = DEFAULT_SESSION_ID

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("\n👋 Goodbye!")
            break

        try:
            response = chain_with_history.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )
            print(f"\nAI: {response.content}\n")

        except Exception as error:
            print(f"\n❌ Error: {type(error).__name__}: {error}\n")
            continue


if __name__ == "__main__":

    chat_loop()
