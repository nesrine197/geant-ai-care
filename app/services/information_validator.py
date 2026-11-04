def normalize_value(value):
    if isinstance(value, str):
        value = value.strip()

        if value.lower() in ["null", "none", "unknown", "not provided", ""]:
            return None

    return value


def validate_information(data: dict) -> dict:
    """
    Validate customer information using Python rules.
    """

    missing_fields = []

    intent = data.get("customer_intent")
    product_type = normalize_value(data.get("product_type"))
    product_model = normalize_value(data.get("product_model"))
    symptoms = data.get("symptoms", [])
    conflicts = data.get("conflicts", [])

    # Rule 1: Check product type
    if not product_type:
        missing_fields.append("product_type")

    # Rule 2: Check customer intent
    if not intent:
        missing_fields.append("customer_intent")

    # Rule 3: Troubleshooting requirements
    if intent == "troubleshooting":

        if not product_model:
            missing_fields.append("product_model")

        if not symptoms:
            missing_fields.append("symptoms")

        # A vague symptom needs clarification
        vague_symptoms = [
            "not working",
            "problem",
            "not functioning",
            "doesn't work"
        ]

        if symptoms and all(
            symptom.strip().lower() in vague_symptoms
            for symptom in symptoms
        ):
            missing_fields.append("specific_symptoms")

    # Rule 4: Detect contradictory information
    if conflicts:
        missing_fields.append("conflicting_information")

    # Final decision
    is_complete = len(missing_fields) == 0

    if is_complete:
        next_action = "safety_check"
    else:
        next_action = "ask_follow_up"

    return {
        "missing_fields": missing_fields,
        "is_complete": is_complete,
        "next_action": next_action
    }
