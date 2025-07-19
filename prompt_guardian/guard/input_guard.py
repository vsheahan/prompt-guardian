import requests
import os

def load_prompt_template():
    base_dir = os.path.dirname(__file__)
    prompt_path = os.path.join(base_dir, "prompts", "input_check.txt")
    with open(prompt_path, "r") as f:
        return f.read()

def guard_input(user_input: str) -> str:
    prompt = load_prompt_template().format(user_input=user_input)

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    raw_response = response.json()["response"].strip()
    normalized = raw_response.upper()

    if normalized.startswith("BLOCK"):
        return "BLOCK"
    elif normalized.startswith("REWRITE:"):
        return raw_response  # keep full rewrite string
    elif normalized.startswith("ALLOW"):
        return "ALLOW"
    elif "BLOCK" in normalized:
        return "BLOCK"
    else:
        return "ALLOW"