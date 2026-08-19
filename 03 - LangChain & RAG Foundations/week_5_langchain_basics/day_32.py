"""
Day 32 - LangChain Agents & Tools

Goal: Build a LangChain agent that picks the right tool based on
the user's question, and uses it to compute the answer.

This script uses the modern LangChain v1+ create_agent API.

This script demonstrates:
- The @tool decorator for creating tools
- Multiple tools: calculator, word counter, date/time
- Modern create_agent (replaces deprecated create_react_agent)
- Real-world multi-tool agent execution

Author: Tejoz
"""

import math
import os
import sys
from datetime import datetime

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
TEMPERATURE = 0.2
TIMEOUT = 30


# ============================================================
# ENVIRONMENT
# ============================================================

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
# TOOL DEFINITIONS
# ============================================================

@tool
def calculate_percentage(percent: float, number: float) -> str:
    """Calculate a percentage of a number.

    Use this when the user asks what X% of Y is.
    Example: 'What's 15% of 240?' → use calculate_percentage(15, 240)
    """
    result = (percent / 100) * number
    return f"{percent}% of {number} is {result}"


@tool
def calculate_square_root(number: float) -> str:
    """Calculate the square root of a number.

    Use this when the user asks for a square root.
    Example: 'What's the square root of 144?' → use calculate_square_root(144)
    """
    if number < 0:
        return "Cannot calculate square root of a negative number."
    result = math.sqrt(number)
    return f"The square root of {number} is {result}"


@tool
def count_words(text: str) -> str:
    """Count the number of words in a text.

    Use this when the user asks how many words are in a text.
    """
    words = text.split()
    word_count = len(words)
    return f"The text contains {word_count} words."


@tool
def get_current_datetime() -> str:
    """Get the current date and time.

    Use this when the user asks what time/date it is now.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


@tool
def add_numbers(a: float, b: float) -> str:
    """Add two numbers together.

    Use this when the user asks for the sum of two numbers.
    """
    return f"{a} + {b} = {a + b}"


# Collect all tools
tools = [
    calculate_percentage,
    calculate_square_root,
    count_words,
    get_current_datetime,
    add_numbers,
]


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
# SYSTEM MESSAGE
# ============================================================

system_message = (
    "You are a helpful AI assistant with access to several tools. "
    "Use the appropriate tool when needed to answer questions accurately. "
    "If a tool gives you the answer, respond with that answer in natural language."
)


# ============================================================
# AGENT SETUP (Modern LangChain v1+ API)
# ============================================================

agent_executor = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_message,
)


# ============================================================
# DEMO
# ============================================================

SAMPLE_QUERIES = [
    "What is 15% of 240?",
    "What's the square root of 144?",
    "How many words are in this sentence: 'LangChain agents are powerful and fun to build'?",
    "What is the current date and time?",
    "What is 87 plus 156?",
]


def run_query(query: str) -> None:
    """Run a single query through the agent."""

    print("\n" + "=" * 60)
    print(f"❓ QUERY: {query}")
    print("=" * 60)

    try:
        result = agent_executor.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )

        # Extract the final AI message
        final_message = result["messages"][-1]
        final_answer = (
            final_message.content
            if hasattr(final_message, "content")
            else str(final_message)
        )

        print(f"\n✅ ANSWER: {final_answer}\n")

    except Exception as error:
        print(f"\n❌ Error: {type(error).__name__}: {error}\n")


if __name__ == "__main__":

    print("=" * 60)
    print("🦜 LangChain Day 32 — Agents & Tools")
    print("=" * 60)
    print("\nRunning sample queries through the agent...\n")

    for query in SAMPLE_QUERIES:
        run_query(query)

    print("\n" + "=" * 60)
    print("✅ Day 32 demo complete!")
    print("=" * 60)
