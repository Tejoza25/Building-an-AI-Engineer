"""
Day 16 - Tool Calling with Python

Author: Tejoz

Description:
This project demonstrates the concept of AI tool calling.
The chatbot decides when to use a calculator tool,
executes it in Python, and then uses the result to
generate a final response.
"""

import os
import re
from dotenv import load_dotenv
from openai import OpenAI

# -------------------------------------------------
# Load environment variables
# -------------------------------------------------
load_dotenv()

# -------------------------------------------------
# Create OpenRouter client
# -------------------------------------------------
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# -------------------------------------------------
# Calculator Tool
# -------------------------------------------------
def calculate(expression):
    """
    Calculates a simple mathematical expression.
    Example:
    25+30
    100/5
    9*8
    """

    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Invalid mathematical expression."


# -------------------------------------------------
# System Prompt
# -------------------------------------------------
system_prompt = """
You are an AI assistant.

Rules:

1. If the user's question contains a simple mathematical expression
   such as +, -, *, or /, respond ONLY with:

CALL_CALCULATOR: expression

Example:
CALL_CALCULATOR: 25+18

2. For every other question,
respond normally.
"""

# -------------------------------------------------
# Get user input
# -------------------------------------------------
user_question = input("You: ")

# -------------------------------------------------
# First request to the LLM
# -------------------------------------------------
response = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_question
        }
    ]
)

assistant_reply = response.choices[0].message.content

# -------------------------------------------------
# Check if calculator tool is needed
# -------------------------------------------------
if assistant_reply.startswith("CALL_CALCULATOR:"):

    expression = assistant_reply.replace(
        "CALL_CALCULATOR:",
        ""
    ).strip()

    tool_result = calculate(expression)

    print("\n🧮 Calculator Tool")
    print("Expression :", expression)
    print("Result     :", tool_result)

    # ---------------------------------------------
    # Send tool result back to the LLM
    # ---------------------------------------------
    final_response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": user_question
            },
            {
                "role": "assistant",
                "content": assistant_reply
            },
            {
                "role": "user",
                "content":
                f"The calculator returned this result: {tool_result}. "
                "Please answer the original question naturally."
            }
        ]
    )

    print("\n🤖 Final Answer:")
    print(final_response.choices[0].message.content)

else:

    print("\n🤖 Bot:")
    print(assistant_reply)