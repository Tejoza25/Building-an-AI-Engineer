import os
import time
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

system_prompt = """
You are a customer support chatbot for Apple AirPods Pro.

Rules:
- Answer ONLY questions about Apple AirPods Pro.
- Politely refuse unrelated questions.
- Keep responses friendly, professional, and concise.
"""

user_question = input("Ask about Apple AirPods Pro: ")

start_time = time.time()

response = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_question}
    ],
    stream=True
)

print("\n🤖 Bot:\n")

for chunk in response:

    if not chunk.choices:
        continue

    delta = chunk.choices[0].delta

    if delta.content:
        print(delta.content, end="", flush=True)

end_time = time.time()

print(f"\n\nResponse time: {end_time - start_time:.2f} seconds")