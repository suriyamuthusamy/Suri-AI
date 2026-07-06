from search import web_search
from ai import get_ai_response
from utils import print_sources, print_response_time
import time

print("🤖 Welcome to Suri AI")
print("Type 'exit' to quit.")
print("Type '/clear' to clear chat history.\n")

chat_history = []

while True:
    question = input("You: ")

    if question.lower() == "exit":
        print("👋 Bye!")
        break

    if question.lower() == "/clear":
        chat_history.clear()
        print("🧹 Conversation history cleared!")
        print("-" * 60)
        continue

    start_time = time.time()

    print("\n🔍 Searching the web...\n")

    context, results = web_search(question)

    messages = [
        {
            "role": "system",
            "content": f"""
You are Suri AI, an intelligent AI assistant.

Use:
- Conversation history
- Web search information

Rules:
- Answer accurately.
- Use previous conversation for follow-up questions.
- Never make up facts.
- Keep answers simple.

Web Information:

{context}
"""
        }
    ]

    messages.extend(chat_history)

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    answer = get_ai_response(messages)

    print_sources(results)

    print_response_time(start_time)

    # Save conversation history
    chat_history.append(
        {
            "role": "user",
            "content": question
        }
    )

    chat_history.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Keep only the last 10 messages (5 conversations)
    if len(chat_history) > 10:
        chat_history = chat_history[-10:]