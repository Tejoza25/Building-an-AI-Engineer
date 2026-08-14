"""
Day 14 - AI Product Support Chatbot (Refactored)

Author: Tejoz

Description:
A customer support chatbot for Apple AirPods Pro built using
the OpenRouter API. The chatbot streams responses in real time
to provide a smooth conversational experience.

Key Features:
- Secure API key management using .env
- System prompt to control chatbot behavior
- Real-time streaming responses
- Response time measurement
"""

import os
import time

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
# Define chatbot behavior
# -------------------------------------------------
system_prompt = """
You are a customer support chatbot for Apple AirPods Pro.

Rules:
- Answer ONLY questions related to Apple AirPods Pro.
- Politely refuse unrelated questions.
- Be friendly, professional, and concise.
"""


# -------------------------------------------------
# Get user input
# -------------------------------------------------
user_question = input("🎧 Ask about Apple AirPods Pro: ")


# -------------------------------------------------
# Start response timer
# -------------------------------------------------
start_time = time.time()


# -------------------------------------------------
# Send request to OpenRouter API
# -------------------------------------------------
chat_response = client.chat.completions.create(
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
    ],
    stream=True
)


# -------------------------------------------------
# Stream AI response
# -------------------------------------------------
print("\n🤖 Bot:\n")

for chunk in chat_response:

    if not chunk.choices:
        continue

    delta = chunk.choices[0].delta

    if delta.content:
        print(delta.content, end="", flush=True)


# -------------------------------------------------
# Display response time
# -------------------------------------------------
end_time = time.time()

print(f"\n\n⏱ Response Time: {end_time - start_time:.2f} seconds")