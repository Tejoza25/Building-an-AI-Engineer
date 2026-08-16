"""
Day 29 - LangChain Fundamentals

Goal: Build my first LangChain-powered LLM chain using OpenRouter.

Compatible with LangChain v1.3+ (modern LCEL syntax).

This script demonstrates:
- Prompt Templates (langchain_core)
- LLM Chains using LCEL (LangChain Expression Language)
- Output Parsers
- LangChain vs raw OpenAI SDK comparison

Author: Tejoz
"""

import os
import sys

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "nvidia/nemotron-3-ultra-550b-a55b:free"
TEMPERATURE = 0.3
TIMEOUT = 30


# ============================================================
# ENVIRONMENT
# ============================================================

import os
from pathlib import Path

# Look for .env in the parent directory (module folder)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)



api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ OPENROUTER_API_KEY is not set.")
    print("Please create a .env file and add your OpenRouter API key.")
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
# PROMPT TEMPLATE
# ============================================================

prompt = PromptTemplate(
    input_variables=["topic"],
    template=(
        "You are a knowledgeable AI tutor.\n"
        "\n"
        "Explain the following topic in exactly 3 short bullet points.\n"
        "\n"
        "Topic: {topic}\n"
        "\n"
        "Format:\n"
        "- [First key idea]\n"
        "- [Second key idea]\n"
        "- [Third key idea]\n"
    ),
)


# ============================================================
# CHAIN SETUP (LCEL — Modern LangChain Syntax)
# ============================================================

output_parser = StrOutputParser()

# LCEL chain: prompt → llm → output_parser
# The | operator pipes data through each component
chain = prompt | llm | output_parser


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("🦜 LangChain Day 29 — First LangChain Chain")
    print("=" * 60)

    topic = input("\nEnter a topic to learn about: ").strip()

    if not topic:
        print("❌ Please enter a topic.")
        sys.exit(1)

    print(f"\n⏳ Generating 3-bullet summary for: {topic}\n")

    try:
        # LCEL uses .invoke() with a dict
        result = chain.invoke({"topic": topic})

        print("=" * 60)
        print("📘 Summary:")
        print("=" * 60)
        print(result)
        print()

    except Exception as error:
        print("\n❌ Chain execution failed.")
        print(f"Error type: {type(error).__name__}")
        print(f"Error details: {error}")
        sys.exit(1)
