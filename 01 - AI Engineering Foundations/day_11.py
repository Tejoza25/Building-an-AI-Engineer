import os
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

- Answer ONLY questions related to Apple AirPods Pro.
- If the question is unrelated, politely refuse.
- Be friendly and professional.
- Keep answers short and easy to understand.
"""
user_question = input("Ask about Apple AirPods Pro: ")

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

print("\nFull Response:")
print(response)
print("\nBot:")

if response.choices:
    print(response.choices[0].message.content)
else:
    print("No response received from the model.")
    print(response)