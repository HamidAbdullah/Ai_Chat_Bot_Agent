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


def identity_override(user_input: str) -> str:
    """Return fixed founder identity answers."""
    text = user_input.strip().lower()
    founder_answer = "Hamid Abdullah is the Founder of Kivyx AI Agent."

    founder_triggers = [
        "who is your founder",
        "who's your founder",
        "who founded you",
        "who made you",
        "founder",
        "hamid abdullah",
    ]
    if any(trigger in text for trigger in founder_triggers):
        return founder_answer

    agent_triggers = [
        "who are you",
        "what are you",
        "what is kivyx ai agent",
        "who made this ai agent",
        "who made this agent",
    ]
    if any(trigger in text for trigger in agent_triggers):
        return "I am Kivyx AI Agent, and Hamid Abdullah is the Founder of Kivyx AI Agent."

    return ""


while True:

    # User input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "exit":
        print("Agent: Bye 👋")
        break

    fixed_identity = identity_override(user_input)
    if fixed_identity:
        print("\nAgent:", fixed_identity)
        print()
        continue

    # Send to AI
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Kivyx AI Agent, a smart and helpful AI assistant. "
                    "If asked who your founder is, say: "
                    "Hamid Abdullah is the Founder of Kivyx AI Agent. "
                    "If asked who Hamid Abdullah is in relation to this AI, say: "
                    "Hamid Abdullah is the Founder of Kivyx AI Agent."
                )
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