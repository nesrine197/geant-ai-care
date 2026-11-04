
def route_after_safety(state):
    classification = state["safety_classification"]

    if classification == "no_safety_concern":
        return "continue"

    if classification == "safety_concern":
        return "escalate"

    return "clarify"


def route_after_validation(state):
    if state["is_complete"]:
        return "complete"

    return "incomplete"
