
from app.agents.questioning_agent import generate_follow_up


missing_fields = [
    "product_model"
]

conversation_history = [
    {
        "role": "user",
        "content": "My Géant TV has a black screen."
    }
]

question = generate_follow_up(
    missing_fields,
    conversation_history
)

print("\n===== AGENT 2 RESULT =====")
print(question)
