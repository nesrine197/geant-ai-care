from app.services.ollama import generate_structured_response


SAFETY_CLASSIFICATION_PROMPT = """
You are the Safety Classification Agent for Géant AI Care.

Analyze the complete customer conversation and identify
potential safety concerns related to the product.

Classify the situation into one of these categories:

- safety_concern
- no_safety_concern
- unclear

Potential concerns include:
- Smoke or burning smell
- Sparks or unusual electrical behavior
- Electric shock
- Fire or overheating
- Gas leakage or suspected gas hazard
- Other immediate product-related danger

RULES:

1. Analyze the complete conversation history.

2. Never invent a safety concern.

3. Use "safety_concern" when the customer reports
   a potential immediate danger.

4. Use "no_safety_concern" when the customer reports
   an ordinary product malfunction without mentioning
   any potential danger.

5. Use "unclear" only when the customer's description
   is genuinely ambiguous regarding a potential hazard.

6. A product not cooling, not starting, or not displaying
   an image does not automatically indicate a safety concern.

7. Do not provide troubleshooting instructions.

8. Do not diagnose the technical problem.
9. If the customer describes a vague or unusual behavior
   without explaining what is happening, classify it as "unclear".

10. Do not classify vague descriptions such as:
    - "My refrigerator is behaving strangely."
    - "Something unusual is happening."
    - "My appliance is acting weird."
    as "no_safety_concern".

11. Use "no_safety_concern" only when the described
    situation is sufficiently clear and no potential
    safety concern is indicated.
Return ONLY valid JSON:

{
    "classification": "no_safety_concern",
    "reason": "No immediate safety concern was reported."
}
"""


def classify_safety(conversation_history: list[dict]):

    response = generate_structured_response(
        conversation_history,
        SAFETY_CLASSIFICATION_PROMPT
    )

    import json

    try:
        data = json.loads(response)
    except json.JSONDecodeError as error:
        raise ValueError(
            "Safety Agent returned invalid JSON."
        ) from error

    allowed_categories = [
        "safety_concern",
        "no_safety_concern",
        "unclear"
    ]

    if data.get("classification") not in allowed_categories:
        raise ValueError("Invalid safety classification.")

    if not isinstance(data.get("reason"), str):
        raise ValueError("Safety reason must be a string.")

    return data

def generate_safety_response(reason: str):

    return (
        "Your safety is important. Based on what you described, "
        "there may be a safety concern with your appliance.\n\n"
        "Please stop using the appliance. If you can do so "
        "without approaching danger, disconnect its power. "
        "If there is smoke, fire, or immediate danger, move "
        "away and contact local emergency services.\n\n"
        "Do not open or attempt to repair the appliance. "
        "Please contact Géant customer support for assistance."
    )