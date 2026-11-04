from langchain_core.messages import HumanMessage
from app.graph.workflow import customer_support_graph

result = customer_support_graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="My refrigerator does not get cold."
            )
        ]
    },
    config={
        "configurable": {
            "thread_id": "refrigerator-test-001"
        }
    }
)

print("\n========== WORKFLOW RESULT ==========")
print("Product:", result.get("product_type"))
print("Model:", result.get("product_model"))
print("Symptoms:", result.get("symptoms"))
print("Missing fields:", result.get("missing_fields"))
print("Complete:", result.get("is_complete"))
print("Agent 2:", result.get("follow_up_question"))
print("Next action:", result.get("next_action"))
print("=====================================")