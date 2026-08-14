import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

from openai import OpenAI

# Connect to OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Send a message to Claude
response = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages=[{
        "role": "user",
        "content": "Hello! What can you do?"
    }]
)

# Print the reply
print(response.choices[0].message.content)
