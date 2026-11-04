from app.graph.state import CustomerSupportState

state: CustomerSupportState = {
    "messages": [],
    "customer_intent": "troubleshooting",
    "product_type": "TV",
    "product_model": None,
    "symptoms": ["TV is not working"],
    "error_code": None,
    "missing_fields": ["product_model"],
    "is_complete": False,
    "follow_up_question": None,
    "next_action": "ask_follow_up"
}

print("Géant AI Care State:")
print(state)