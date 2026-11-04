from langchain_core.messages import HumanMessage
from app.graph.workflow import customer_support_graph

config = {
    "configurable": {
        "thread_id": "refrigerator-test-002"
    }
}

# First customer message
result1 = customer_support_graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="My refrigerator does not get cold."
            )
        ]
    },
    config=config
)

print("\n--- FIRST MESSAGE ---")
print("Model:", result1.get("product_model"))
print("Question:", result1.get("follow_up_question"))

# Second customer message
result2 = customer_support_graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="The model is GTV-450."
            )
        ]
    },
    config=config
)

print("\n--- SECOND MESSAGE ---")
print("Product:", result2.get("product_type"))
print("Model:", result2.get("product_model"))
print("Symptoms:", result2.get("symptoms"))
print("Missing fields:", result2.get("missing_fields"))
print("Complete:", result2.get("is_complete"))
print("Next action:", result2.get("next_action"))