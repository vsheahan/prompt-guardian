import requests
import re
from prompt_guardian.guard.output_guard import guard_output
from prompt_guardian.guard.input_guard import guard_input

def call_ollama(prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()


# Static output filter for suspicious commands
def is_suspicious_output(text: str) -> bool:
    suspicious_keywords = [
        r"\brm\b", r"\bcd\b", r"\bls\b", r"\bsudo\b",
        r"\bchmod\b", r"\btouch\b", r"\bmkdir\b", r"\bapt\b",
        r"\bnano\b", r"\bpwd\b", r"\bcat\b", r"\bmv\b"
    ]
    for pattern in suspicious_keywords:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    return False

from datetime import datetime
import os

def log_blocked(prompt_type, content):
    print(f"Logging blocked event [{prompt_type}]: {content}")
    log_dir = "guard/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "blocked_prompts.log")
    with open(log_path, "a") as log_file:
        log_file.write(f"[{datetime.now()}] [{prompt_type}] {content}\n")

def run_secure_conversation(user_input):
    guard_decision = guard_input(user_input)
    print(f">>> Guard decision: {guard_decision}")

    if guard_decision.startswith("BLOCK"):
        log_blocked("INPUT", user_input)
        return "[Blocked by guard: suspected injection.]"
    elif guard_decision.startswith("REWRITE:"):
        user_input = guard_decision[len("REWRITE:"):].strip()

    model_output = call_ollama(user_input)

    if is_suspicious_output(model_output):
        log_blocked("STATIC OUTPUT", model_output)
        return "[Blocked by static policy: command detected]"

    return model_output


