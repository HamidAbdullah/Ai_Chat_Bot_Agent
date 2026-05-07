import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Groq client setup
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

print("🤖 AI Agent Started")
print("Type 'exit' to stop\n")

while True:

    # User input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "exit":
        print("Agent: Bye 👋")
        break

    # Send to AI
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    # Print AI response
    print("\nAgent:", response.choices[0].message.content)
    print()