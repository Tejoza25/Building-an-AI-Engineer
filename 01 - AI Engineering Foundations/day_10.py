import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

prompt = """
You are an AI assistant that extracts structured information.

Return ONLY valid JSON.

Extract the following fields:

- customer_name
- order_number
- ordered_product
- received_product
- issue
- email
- phone

Customer Message:

Hello Support Team,

My name is Sarah Johnson, and I'm writing regarding my recent purchase.

I placed an order for a Dell Inspiron 15 Laptop on July 18, 2026.

Unfortunately, when my package arrived today, I received an HP Pavilion Laptop instead.

My order number is ORD-784521.

I would appreciate it if you could arrange a replacement as soon as possible.

You can reach me at sarah.johnson@email.com or +1-555-123-4567.

Thank you for your assistance.

Best regards,
Sarah Johnson
"""
response = client.chat.completions.create(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

ai_reply = response.choices[0].message.content

print("Structured JSON Output")
print("-" * 40)
print(ai_reply)