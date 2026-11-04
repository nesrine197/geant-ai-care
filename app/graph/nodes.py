
from langchain_core.messages import AIMessage

from app.agents.language_agent import detect_language
from app.agents.information_agent import extract_information
from app.agents.questioning_agent import generate_follow_up
from app.agents.safety_agent import classify_safety
from app.agents.safety_response_agent import generate_safety_response

from app.services.information_validator import validate_information


# ==========================================
# HELPER: Convert LangGraph messages
# ==========================================

def convert_messages_to_history(messages):
    """Convert LangGraph messages into Ollama-compatible messages."""

    history = []

    for message in messages:

        if isinstance(message, dict):
            role = message.get("role", "user")
            content = message.get("content", "")

        else:
            role = getattr(message, "type", "human")
            content = message.content

            if role == "human":
                role = "user"

            elif role == "ai":
                role = "assistant"

        history.append({
            "role": role,
            "content": content
        })

    return history


# ==========================================
# NODE 0: Language Agent
# ==========================================

def language_node(state):

    history = convert_messages_to_history(state["messages"])

    latest_message = next(
        (
            message["content"]
            for message in reversed(history)
            if message["role"] == "user"
        ),
        ""
    )

    language = detect_language([
        {
            "role": "user",
            "content": latest_message
        }
    ])

    return {
        "language": language
    }


# ==========================================
# NODE 1: Information Agent
# ==========================================

def information_node(state):

    history = convert_messages_to_history(state["messages"])

    print("\n========== HISTORY SENT TO AGENT 1 ==========")
    print(history)
    print("==============================================")

    result = extract_information(history)

    return {
        "customer_intent": result["customer_intent"],
        "product_type": result["product_type"],
        "product_model": result["product_model"],
        "symptoms": result["symptoms"],
        "error_code": result["error_code"],
        "conflicts": result["conflicts"]
    }


# ==========================================
# NODE 2: Safety Agent
# ==========================================

def safety_node(state):

    history = convert_messages_to_history(state["messages"])

    result = classify_safety(history)

    return {
        "safety_classification": result["classification"],
        "safety_reason": result["reason"]
    }


# ==========================================
# NODE 3: Safety Response
# ==========================================

def safety_response_node(state):

    response = generate_safety_response(
        state["safety_reason"],
        state["language"]
    )

    return {
        "messages": [
            AIMessage(content=response)
        ],
        "next_action": "safety_escalation"
    }


# ==========================================
# NODE 4: Safety Clarification
# ==========================================

def safety_clarification_node(state):

    clarification_messages = {

        "en": (
            "I'd like to understand the situation better. "
            "Have you noticed anything unusual, such as smoke, "
            "sparks, an unusual smell, or excessive heat?"
        ),

        "fr": (
            "J'aimerais mieux comprendre la situation. "
            "Avez-vous remarqué quelque chose d'inhabituel, "
            "comme de la fumée, des étincelles, une odeur "
            "anormale ou une chaleur excessive ?"
        ),

        "ar": (
            "أود فهم الوضع بشكل أفضل. هل لاحظت أي شيء غير "
            "طبيعي، مثل الدخان أو الشرر أو رائحة غير معتادة "
            "أو حرارة مرتفعة؟"
        )
    }

    language = state.get("language", "en")

    question = clarification_messages.get(
        language,
        clarification_messages["en"]
    )

    return {
        "messages": [
            AIMessage(content=question)
        ],
        "follow_up_question": question,
        "next_action": "safety_clarification"
    }


# ==========================================
# NODE 5: Python Information Validator
# ==========================================

def validation_node(state):

    result = validate_information({

        "customer_intent": state["customer_intent"],
        "product_type": state["product_type"],
        "product_model": state["product_model"],
        "symptoms": state["symptoms"],
        "error_code": state["error_code"],
        "conflicts": state.get("conflicts", [])

    })

    return {
        "missing_fields": result["missing_fields"],
        "is_complete": result["is_complete"],
        "next_action": result["next_action"]
    }


# ==========================================
# NODE 6: Customer Questioning Agent
# ==========================================

def questioning_node(state):

    history = convert_messages_to_history(state["messages"])

    question = generate_follow_up(
        state["missing_fields"],
        history,
        state["language"]
    )

    return {
        "follow_up_question": question,
        "messages": [
            AIMessage(content=question)
        ]
    }
