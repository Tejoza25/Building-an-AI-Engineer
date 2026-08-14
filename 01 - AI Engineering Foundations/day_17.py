"""
====================================================
Day 16 - AI Agent with Calculator Tool
Author: Tejoz

Description:
This project demonstrates how an AI Agent can use
a Python calculator tool to solve mathematical
questions and use an LLM for all other questions.

Concept:
Agent = LLM + Tool
====================================================
"""

import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# ----------------------------------------
# Load API Key
# ----------------------------------------
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# ----------------------------------------
# Calculator Tool
# ----------------------------------------
def calculator(user_input):
    """
    Handles percentage questions.

    Example:
    23% of 1847
    """

    pattern = r"(\d+(\.\d+)?)%\s*of\s*(\d+(\.\d+)?)"

    match = re.search(pattern, user_input.lower())

    if match:

        percentage = float(match.group(1))
        number = float(match.group(3))

        answer = (percentage / 100) * number

        return (
            f"{percentage}% of {number} is "
            f"{answer:.2f}"
        )

    return None


# ----------------------------------------
# AI Chat Function
# ----------------------------------------
def ask_llm(question):

    response = client.chat.completions.create(

        model="nvidia/nemotron-3-ultra-550b-a55b:free",

        messages=[
            {
                "role": "system",
                "content":
                """
                You are a helpful AI assistant.

                If a calculator result is already
                provided, explain it naturally.

                Otherwise answer normally.
                """
            },

            {
                "role": "user",
                "content": question
            }

        ]

    )

    return response.choices[0].message.content


# ----------------------------------------
# Main Program
# ----------------------------------------
print("=" * 50)
print("🤖 AI Agent with Calculator Tool")
print("=" * 50)

while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() == "quit":
        print("\nGoodbye 👋")
        break

    # ------------------------------------
    # Tool Decision
    # ------------------------------------
    tool_result = calculator(user_input)

    if tool_result:

        print("\n🧮 Calculator Tool Used")
        print(tool_result)

        final_prompt = f"""
The user asked:

{user_input}

Calculator result:

{tool_result}

Please answer naturally.
"""

        ai_response = ask_llm(final_prompt)

    else:

        ai_response = ask_llm(user_input)

    print("\n🤖 Agent:")
    print(ai_response)