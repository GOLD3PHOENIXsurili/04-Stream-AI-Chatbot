import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables (.env)
load_dotenv()

# Create client (Groq via OpenAI-compatible API)
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

messages = []
EXIT_COMMANDS = ["exit", "quit", "bye"]

while True:
    user_input = input("\nYou: ")

    if not user_input.strip():
        continue

    if user_input.lower() in EXIT_COMMANDS:
        print("\nAssistant: Goodbye! 👋")
        break

    messages.append({"role": "user", "content": user_input})

    # Stream tokens instead of waiting for the full response
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True
    )

    assistant_reply = ""
    print("\nAssistant: ", end="", flush=True)

    # Each chunk.delta.content is the newly generated text, not the full message
    for chunk in response:
        token = chunk.choices[0].delta.content
        if token:
            print(token, end="", flush=True)
            assistant_reply += token

    print()

    # Save assistant reply so the model remembers its own previous turns
    messages.append({"role": "assistant", "content": assistant_reply})