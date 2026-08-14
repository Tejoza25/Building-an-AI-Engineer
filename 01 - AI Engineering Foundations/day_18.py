"""
=========================================================
Day 18 - AI Agent with DuckDuckGo Search Tool

Author: Tejoz

Description:
This AI Agent can answer normal questions using an LLM.
If the user asks for recent or factual information,
the agent uses DuckDuckGo Search before answering.

Requirements:
pip install openai python-dotenv duckduckgo-search

=========================================================
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from ddgs import DDGS

# -------------------------------------------------
# Load Environment Variables
# -------------------------------------------------

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# -------------------------------------------------
# DuckDuckGo Search Tool
# -------------------------------------------------

def search_web(query):

    print("\n🔍 Searching the web...\n")

    results = []

    with DDGS() as ddgs:
        search_results = ddgs.text(query, max_results=5)

        for item in search_results:

            results.append(
                f"Title: {item['title']}\n"
                f"Snippet: {item['body']}\n"
                f"URL: {item['href']}\n"
            )

    return "\n".join(results)

# -------------------------------------------------
# Decide Whether Search Is Needed
# -------------------------------------------------

def needs_search(question):

    keywords = [
        "latest",
        "today",
        "news",
        "current",
        "price",
        "weather",
        "who is",
        "what happened",
        "search",
        "find",
        "look up"
    ]

    question = question.lower()

    for word in keywords:

        if word in question:
            return True

    return False

# -------------------------------------------------
# Chat with LLM
# -------------------------------------------------

def ask_llm(question):

    response = client.chat.completions.create(

        model="nvidia/nemotron-3-ultra-550b-a55b:free",

        messages=[
            {
                "role": "system",
                "content":
                """
                You are a helpful AI assistant.

                If search results are provided,
                use ONLY those search results
                to answer the user's question.

                Keep answers concise.
                """
            },
            {
                "role": "user",
                "content": question
            }
        ]

    )

    return response.choices[0].message.content

# -------------------------------------------------
# Main Program
# -------------------------------------------------

print("=" * 55)
print("🤖 AI Agent with DuckDuckGo Search Tool")
print("=" * 55)

while True:

    user_input = input("\nYou: ").strip()

    if user_input.lower() == "quit":
        print("\n👋 Goodbye!")
        break

    if needs_search(user_input):

        search_results = search_web(user_input)

        prompt = f"""
User Question:

{user_input}

Search Results:

{search_results}

Answer the user's question using the search results above.
"""

        answer = ask_llm(prompt)

    else:

        answer = ask_llm(user_input)

    print("\n🤖 Agent:\n")
    print(answer)