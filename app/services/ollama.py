import requests
from pathlib import Path


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

MODEL_NAME = "gemma3:4b"


# Load Géant AI Care system prompt
SYSTEM_PROMPT_PATH = Path(__file__).with_name("care_system.txt")

SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def generate_response(conversation_history: list[dict]):

    # Start with the system prompt
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    # Add conversation history
    messages.extend(conversation_history)

    # Prepare Ollama request
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    # Send request to Ollama
    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    print("Ollama status:", response.status_code)
    print("Ollama response:", response.text)

    # Check for errors
    response.raise_for_status()

    # Extract Gemma response
    result = response.json()

    return result["message"]["content"]


def generate_structured_response(
    conversation_history: list[dict],
    system_prompt: str
):
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    messages.extend(conversation_history)

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "format": "json",
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    print("\n========== OLLAMA DEBUG ==========")
    print("MODEL:", MODEL_NAME)
    print("DONE REASON:", result.get("done_reason"))
    print("FULL RESPONSE:", result)
    print("==================================\n")

    return result["message"]["content"]