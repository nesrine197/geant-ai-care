
import json

from app.services.ollama import generate_structured_response


QUESTIONING_PROMPT = """
You are Agent 2: Customer Questioning Agent
for Géant AI Care.

Your task is to ask the customer for missing information.

The customer's detected language is: {language}

Language rules:
- en: Ask in English.
- fr: Ask in French.
- ar: Ask in Arabic.
- Always use the detected language.
- For Arabic, use natural Arabic.
- Do not translate product model numbers.

Rules:
1. Ask only about missing information.
2. Ask one question at a time.
3. Never repeat information already provided.
4. Do not provide troubleshooting instructions.
5. Return only valid JSON.

Required format:
{
    "question": "Your question here"
}
"""


def generate_follow_up(
    missing_fields: list[str],
    conversation_history: list[dict],
    language: str
):
    context = {
        "missing_fields": missing_fields,
        "conversation_history": conversation_history
    }

    # Insert the detected language into the prompt.
    system_prompt = QUESTIONING_PROMPT.replace(
        "{language}",
        language
    )

    response = generate_structured_response(
        [
            {
                "role": "user",
                "content": str(context)
            }
        ],
        system_prompt
    )

    try:
        data = json.loads(response)

    except json.JSONDecodeError as error:
        raise ValueError(
            "Agent 2 returned invalid JSON."
        ) from error

    question = data.get("question")

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Agent 2 returned an empty question.")

    return question
