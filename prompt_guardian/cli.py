import argparse
from prompt_guardian.main.llm_wrapper import run_secure_conversation
def main():
    parser = argparse.ArgumentParser(description="Prompt Guardian CLI")
    parser.add_argument("prompt", type=str, help="Prompt to evaluate and submit to the LLM")
    args = parser.parse_args()

    print(">>> prompt-guardian launched (CLI mode)")
    print("You:", args.prompt)
    response = run_secure_conversation(args.prompt)
    print("LLM:", response)

if __name__ == "__main__":
    main()