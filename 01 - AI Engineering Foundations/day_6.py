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

# Store conversation history
conversation_history = []

print("🤖 AI Chatbot is ready!")
print("Type your message and press Enter")
print("Type 'quit' to exit")
print("-" * 40)

# Keep chatting in a loop
while True:

    # Get your message
    user_input = input("You: ").strip()

    # Exit if user types quit
    if user_input.lower() == "quit":
        print("Goodbye! 👋")
        break

    # Skip if empty message
    if user_input == "":
        continue

    # Add your message to history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # Send to AI and get reply
    response = client.chat.completions.create(
        model="nvidia/nemotron-3-ultra-550b-a55b:free",
        messages=conversation_history
    )

    # Get the AI reply
    ai_reply = response.choices[0].message.content

    # Add AI reply to history
    conversation_history.append({
        "role": "assistant",
        "content": ai_reply
    })

    # Print the reply
    print(f"AI: {ai_reply}")
    print("-" * 40)