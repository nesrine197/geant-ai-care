import json

from app.services.ollama import generate_structured_response


LANGUAGE_PROMPT = """
You are a Language Detection Agent for Géant AI Care.

Identify the language used in the customer's latest message.

Supported languages:
- en = English
- fr = French
- ar = Arabic

Rules:
1. Detect the actual language of the customer's message.
2. Do not translate the message.
3. If the customer mixes languages, identify the dominant language.
4. Return only valid JSON.

Required format:

{
    "language": "en"
}
"""


def detect_language(conversation_history: list[dict]):

    response = generate_structured_response(
        conversation_history,
        LANGUAGE_PROMPT
    )

    try:
        data = json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Language Agent returned invalid JSON."
        ) from error

    language = data.get("language")

    if language not in ["en", "fr", "ar"]:
        raise ValueError("Unsupported language detected.")

    return language