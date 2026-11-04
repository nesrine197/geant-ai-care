
from langchain_core.messages import HumanMessage

from app.graph.workflow import customer_support_graph


def run_workflow(message, thread_id):

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    result = customer_support_graph.invoke(
        {
            "messages": [
                HumanMessage(content=message)
            ]
        },
        config=config
    )

    print("\nCUSTOMER:", message)
    print("LANGUAGE:", result.get("language"))
    print("SAFETY:", result.get("safety_classification"))
    print("ACTION:", result.get("next_action"))

    print("\nASSISTANT RESPONSE:")

    for msg in result["messages"]:
        if getattr(msg, "type", None) == "ai":
            print(msg.content)

    return result


def test_normal_malfunction():

    result = run_workflow(
        "My refrigerator does not get cold.",
        "normal-test"
    )

    assert result["safety_classification"] == "no_safety_concern"


def test_safety_concern():

    result = run_workflow(
        "I smell something burning near my refrigerator.",
        "safety-test"
    )

    assert result["safety_classification"] == "safety_concern"
    assert result["next_action"] == "safety_escalation"


def test_unclear_situation():

    result = run_workflow(
        "My refrigerator is behaving strangely.",
        "unclear-test"
    )

    assert result["safety_classification"] == "unclear"
    assert result["next_action"] == "safety_clarification"
