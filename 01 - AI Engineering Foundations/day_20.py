"""
=========================================================
Day 20 - AI Memory: Short-Term, Long-Term & Semantic Memory

Author: Tejoz

Description:
A simple file-based memory system demonstrating:

1. Short-Term Memory
2. Long-Term Memory
3. Semantic Memory

The project uses JSON files to persist information
between application sessions.

=========================================================
"""

import json
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI


# -------------------------------------------------------
# Configuration
# -------------------------------------------------------

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

MEMORY_FILE = "memory.json"


# -------------------------------------------------------
# File-Based Memory
# -------------------------------------------------------

def load_memory():
    """
    Load saved memory from the JSON file.
    """

    if not os.path.exists(MEMORY_FILE):
        return {
            "long_term": [],
            "semantic": []
        }

    try:

        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):

        return {
            "long_term": [],
            "semantic": []
        }


def save_memory(memory):
    """
    Save memory to the JSON file.
    """

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


# -------------------------------------------------------
# Short-Term Memory
# -------------------------------------------------------

conversation_history = []


def add_to_short_term_memory(role, content):
    """
    Store messages for the current conversation.
    """

    conversation_history.append(
        {
            "role": role,
            "content": content
        }
    )


# -------------------------------------------------------
# Long-Term Memory
# -------------------------------------------------------

def save_long_term_memory(memory, user_message):
    """
    Save important conversation information
    so it survives future sessions.
    """

    memory["long_term"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "message": user_message
        }
    )

    save_memory(memory)


# -------------------------------------------------------
# Semantic Memory
# -------------------------------------------------------

def extract_facts(user_message):
    """
    Very simple rule-based fact extraction.

    This is intentionally basic for learning purposes.
    More advanced systems can use an LLM or embeddings.
    """

    patterns = [
        r"my name is (.+)",
        r"i am learning (.+)",
        r"i work as (.+)",
        r"i live in (.+)",
        r"i like (.+)"
    ]

    facts = []

    text = user_message.lower().strip()

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:

            fact = match.group(0)

            facts.append(fact)

    return facts


def save_semantic_memory(memory, facts):
    """
    Store extracted facts as semantic memory.
    """

    for fact in facts:

        if fact not in memory["semantic"]:

            memory["semantic"].append(fact)

    save_memory(memory)


def retrieve_relevant_memory(memory, query):
    """
    Retrieve simple keyword-based relevant memories.

    This is a beginner implementation.
    Production systems can use embeddings/vector databases.
    """

    query_words = set(
        re.findall(
            r"\b[a-zA-Z]{3,}\b",
            query.lower()
        )
    )

    relevant = []

    for fact in memory["semantic"]:

        fact_words = set(
            re.findall(
                r"\b[a-zA-Z]{3,}\b",
                fact.lower()
            )
        )

        if query_words.intersection(fact_words):

            relevant.append(fact)

    return relevant


# -------------------------------------------------------
# LLM
# -------------------------------------------------------

def ask_llm(user_message, memory):
    """
    Send the user's message together with
    short-term and relevant long-term memory.
    """

    relevant_memory = retrieve_relevant_memory(
        memory,
        user_message
    )

    memory_context = "\n".join(relevant_memory)

    system_prompt = f"""
You are a helpful AI assistant.

You have access to memory about the user.

Relevant long-term/semantic memory:
{memory_context}

Use this information only when it is relevant.

Do not invent memories.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # Add short-term conversation history
    messages.extend(conversation_history)

    response = client.chat.completions.create(

        model="nvidia/nemotron-3-ultra-550b-a55b:free",

        messages=messages
    )

    return response.choices[0].message.content


# -------------------------------------------------------
# Main Application
# -------------------------------------------------------

print("=" * 60)

print("🧠 Day 20 - AI Memory System")

print("=" * 60)

print("""
Memory Types:

1. Short-Term Memory
   → Current conversation

2. Long-Term Memory
   → Saved to memory.json

3. Semantic Memory
   → Relevant facts about the user

Type 'quit' to exit.
""")

memory = load_memory()


while True:

    user_input = input("\nYou: ").strip()

    if not user_input:

        print("Please enter a message.")

        continue

    if user_input.lower() == "quit":

        print("\n👋 Session ended.")

        break

    # -----------------------------------------------
    # Short-Term Memory
    # -----------------------------------------------

    add_to_short_term_memory(
        "user",
        user_input
    )

    # -----------------------------------------------
    # Extract Semantic Facts
    # -----------------------------------------------

    facts = extract_facts(user_input)

    if facts:

        save_semantic_memory(
            memory,
            facts
        )

        print("\n🧠 Memory updated.")

    # -----------------------------------------------
    # Save Long-Term Memory
    # -----------------------------------------------

    save_long_term_memory(
        memory,
        user_input
    )

    # -----------------------------------------------
    # Ask LLM
    # -----------------------------------------------

    answer = ask_llm(
        user_input,
        memory
    )

    # -----------------------------------------------
    # Add Assistant Response
    # -----------------------------------------------

    add_to_short_term_memory(
        "assistant",
        answer
    )

    print("\n🤖 Agent:")
    print(answer)

    print("\n" + "-" * 60)