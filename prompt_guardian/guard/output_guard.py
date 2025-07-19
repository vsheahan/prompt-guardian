import requests
import re

def load_output_guard_prompt():
    return """
You are a strict security filter. Your job is to BLOCK any LLM response that does **any** of the following:

- Contains shell commands (e.g., rm, ls, mkdir, touch, sudo)
- Mentions or explains terminal commands or CLI usage
- Roleplays or simulates technical environments (e.g., a Linux terminal, computer, AI agent)
- Provides code or instructions that could be considered operational or administrative

Respond with:
- "BLOCK" — if any of the above are found
- "PASS" — if none of the above are present

Be extremely strict. Even educational or descriptive references to these behaviors should be BLOCKED.

LLM Output:
\"\"\"{model_output}\"\"\"
"""

def guard_output(model_output: str) -> str:
    prompt = load_output_guard_prompt().format(model_output=model_output)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()

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