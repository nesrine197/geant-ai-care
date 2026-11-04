from langchain_core.messages import HumanMessage
from app.graph.workflow import customer_support_graph

messages = [
    "My refrigerator does not get cold.",
    "Mon réfrigérateur ne refroidit pas.",
    "الثلاجة لا تبرد."
]

for index, message in enumerate(messages):

    result = customer_support_graph.invoke(
        {
            "messages": [
                HumanMessage(content=message)
            ]
        },
        config={
            "configurable": {
                "thread_id": f"language-test-{index}"
            }
        }
    )

    print("\nCustomer:", message)
    print("Detected language:", result.get("language"))