print(">>> test_conversation.py launched")

from main.llm_wrapper import run_secure_conversation

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    print("LLM:", run_secure_conversation(user_input))