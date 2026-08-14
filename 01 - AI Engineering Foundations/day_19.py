"""
=========================================================
Day 19 - Multi-Tool AI Agent (Calculator + DuckDuckGo)

Author: Tejoz

Description:
A simple AI Agent that can:
1. Use a Calculator Tool
2. Search the Web using DuckDuckGo
3. Decide which tool to use
4. Send tool results to the LLM
5. Generate a final natural-language response

Concepts Learned:
- AI Agents
- Tool Selection
- ReAct Loop
- Prompt Engineering
- OpenRouter API
=========================================================
"""

import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from ddgs import DDGS

# ---------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ---------------------------------------------------
# System Prompt
# ---------------------------------------------------

SYSTEM_PROMPT = """
You are a helpful AI assistant.

You may receive results from external tools such as
a calculator or web search.

If tool results are available,
use them to answer accurately.

Do not invent information.

Keep responses concise and easy to understand.
"""

# ---------------------------------------------------
# DuckDuckGo Search Tool
# ---------------------------------------------------

def search_web(query):

    print("\n🔍 Searching DuckDuckGo...\n")

    try:

        results = []

        with DDGS() as ddgs:

            for r in ddgs.text(query, max_results=5):

                results.append(
                    f"""
Title: {r['title']}

Snippet:
{r['body']}

URL:
{r['href']}
"""
                )

        if not results:
            return "No search results found."

        return "\n".join(results)

    except Exception as e:
        return f"Search Error: {e}"


# ---------------------------------------------------
# Calculator Tool
# ---------------------------------------------------

def calculator(question):

    q = question.lower()

    q = q.replace("what is", "")
    q = q.replace("calculate", "")
    q = q.replace("?", "").strip()

    # Percentage calculation
    percent = re.search(
        r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)",
        q
    )

    if percent:

        p = float(percent.group(1))
        n = float(percent.group(2))

        answer = (p / 100) * n

        return f"{p}% of {n} = {answer:.2f}"

    # NOTE:
    # eval() is used only for learning purposes.
    # In production, use a safer parser such as ast.

    expression = re.sub(
        r"[^0-9+\-*/(). ]",
        "",
        q
    )

    if not expression.strip():
        return "No valid mathematical expression found."

    try:

        result = eval(
            expression,
            {"__builtins__": None},
            {}
        )

        return f"{expression} = {result}"

    except Exception as e:

        return f"Calculation Error: {e}"


# ---------------------------------------------------
# Decide Which Tool to Use
# ---------------------------------------------------

def decide_tool(question):

    q = question.lower()

    search_keywords = [

        "latest",
        "today",
        "news",
        "current",
        "weather",
        "price",
        "search",
        "find",
        "look up",
        "who is",
        "where is",
        "when did",
        "latest ai"

    ]

    math_keywords = [

        "calculate",
        "add",
        "subtract",
        "multiply",
        "divide",
        "%"

    ]

    if any(word in q for word in search_keywords):
        return "search"

    if any(word in q for word in math_keywords):
        return "calculator"

    if re.search(r"\d+\s*[\+\-\*/]\s*\d+", q):
        return "calculator"

    return None


# ---------------------------------------------------
# Run Selected Tool
# ---------------------------------------------------

def run_tool(tool, question):

    if tool == "search":
        return search_web(question)

    if tool == "calculator":
        return calculator(question)

    return ""


# ---------------------------------------------------
# Ask LLM
# ---------------------------------------------------

def ask_llm(prompt):

    response = client.chat.completions.create(

        model="nvidia/nemotron-3-ultra-550b-a55b:free",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    return response.choices[0].message.content


# ---------------------------------------------------
# Main Program
# ---------------------------------------------------

print("=" * 60)
print("🤖 Multi-Tool AI Agent")
print("Calculator + DuckDuckGo Search")
print("=" * 60)

while True:

    user = input("\nYou: ").strip()

    if not user:
        print("⚠ Please enter a question.")
        continue

    if user.lower() == "quit":
        print("\n👋 Goodbye!")
        break

    print("\n🧠 Reasoning...")

    tool = decide_tool(user)

    if tool:

        print(f"⚙ Tool Selected: {tool.title()}")

        observation = run_tool(tool, user)

        print("\n📌 Tool Output:\n")
        print(observation)

        prompt = f"""
User Question:
{user}

Tool Used:
{tool}

Tool Output:
{observation}

Using the tool output above,
provide a clear and accurate answer.
"""

        answer = ask_llm(prompt)

    else:

        print("⚙ No tool required.")

        answer = ask_llm(user)

    print("\n🤖 Agent:\n")
    print(answer)

    print("\n" + "-" * 60)