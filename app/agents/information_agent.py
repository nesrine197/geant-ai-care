
import json

from app.services.ollama import generate_structured_response


INFORMATION_EXTRACTION_PROMPT = """
You are an information extraction agent for Géant AI Care.

Analyze the complete conversation history.

Extract:
- customer_intent
- product_type
- product_model
- symptoms
- error_code
- conflicts

Rules:
1. Extract only information explicitly provided by the customer.
2. Preserve information from earlier messages.
3. Never invent product models or symptoms.
4. Use JSON null for unknown values.
5. Use [] when no symptoms or conflicts exist.
6. If two different models are mentioned, record the contradiction in conflicts.
7. Do not answer technical questions.
8. Do not provide troubleshooting instructions.

Allowed customer_intent values:
- troubleshooting
- product_information
- other

Return exactly one JSON object with all six fields.

Example:
{
    "customer_intent": "troubleshooting",
    "product_type": "refrigerator",
    "product_model": "GTV-450",
    "symptoms": ["does not get cold"],
    "error_code": null,
    "conflicts": []
}
"""


def extract_information(conversation_history: list[dict]):

    response = generate_structured_response(
        conversation_history,
        INFORMATION_EXTRACTION_PROMPT
    )

    print("\n========== AGENT 1 DEBUG ==========")
    print("CONVERSATION:", conversation_history)
    print("RAW RESPONSE:", repr(response))

    try:
        data = json.loads(response)

    except json.JSONDecodeError as error:
        raise ValueError(
            "Agent 1 returned invalid JSON."
        ) from error

    if not isinstance(data, dict):
        raise ValueError(
            "Agent 1 must return a JSON object."
        )

    if not data:
        raise ValueError(
            "Agent 1 returned an empty JSON object."
        )

    required_fields = [
        "customer_intent",
        "product_type",
        "product_model",
        "symptoms",
        "error_code",
        "conflicts"
    ]

    for field in required_fields:
        if field not in data:
            raise ValueError(
                f"Agent 1 missing field: {field}"
            )

    if not isinstance(data["symptoms"], list):
        raise ValueError("Symptoms must be a list.")

    if not isinstance(data["conflicts"], list):
        raise ValueError("Conflicts must be a list.")

    print("PARSED DATA:", data)
    print("==================================\n")

    return data