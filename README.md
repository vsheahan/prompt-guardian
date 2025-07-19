<p align="left">
  <img src="./assets/logo.png" alt="Prompt Guardian Logo" height="275">
</p>

# Prompt Guardian


Prompt Guardian is a lightweight CLI tool that acts as a protective layer between users and a local LLM, such as one running via Ollama. It evaluates prompts before they're sent to the model, allowing or blocking based on configurable policy logic.

This project was originally developed as a proof of concept and experiment in building LLM guardrails for local inference environments.

## Features

- Input prompt inspection and policy enforcement
- Support for ALLOW, BLOCK, and REWRITE decisions
- Integration with local LLMs via Ollama HTTP API
- CLI interface for quick testing
- Logging of blocked and rewritten prompts

## Requirements

- Python 3.8+
- Ollama installed and running with a supported model (e.g., mistral)

## Installation

Clone the repository and install it in editable mode:

```
git clone https://github.com/your-username/prompt-guardian.git
cd prompt-guardian
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage

Start the local LLM with:

```
ollama run mistral
```

Then you can run:

```
prompt-guardian "What is the capital of Massachusetts?"
```

The CLI will show whether the prompt was allowed, rewritten, or blocked, and the LLM’s response if applicable.

## Project Structure

- `prompt_guardian/cli.py`: CLI entry point
- `prompt_guardian/main/llm_wrapper.py`: Core orchestration logic
- `prompt_guardian/guard/`: Prompt validation logic
- `prompt_guardian/guard/prompts/input_check.txt`: The prompt policy template
- `examples/test_conversation.py`: Example script for testing

## License

MIT