
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

from app.graph.state import CustomerSupportState

from app.graph.nodes import (
    language_node,
    information_node,
    validation_node,
    questioning_node,
    safety_node,
    safety_response_node,
    safety_clarification_node
)

from app.graph.edges import (
    route_after_validation,
    route_after_safety
)


def build_workflow():

    graph = StateGraph(CustomerSupportState)

    # =====================================
    # 1. Register nodes
    # =====================================

    graph.add_node("language", language_node)
    graph.add_node("information", information_node)
    graph.add_node("safety", safety_node)
    graph.add_node("safety_response", safety_response_node)
    graph.add_node("safety_clarification", safety_clarification_node)
    graph.add_node("validation", validation_node)
    graph.add_node("questioning", questioning_node)

    # =====================================
    # 2. Initial flow
    # =====================================

    graph.add_edge(START, "language")
    graph.add_edge("language", "information")
    graph.add_edge("information", "safety")

    # =====================================
    # 3. Safety routing
    # =====================================

    graph.add_conditional_edges(
        "safety",
        route_after_safety,
        {
            "continue": "validation",
            "escalate": "safety_response",
            "clarify": "safety_clarification"
        }
    )

    # =====================================
    # 4. Safety response and clarification
    # =====================================

    graph.add_edge("safety_response", END)
    graph.add_edge("safety_clarification", END)

    # =====================================
    # 5. Information validation
    # =====================================

    graph.add_conditional_edges(
        "validation",
        route_after_validation,
        {
            "complete": END,
            "incomplete": "questioning"
        }
    )

    # =====================================
    # 6. Customer questioning
    # =====================================

    graph.add_edge("questioning", END)

    # =====================================
    # 7. Memory
    # =====================================

    checkpointer = InMemorySaver()

    return graph.compile(checkpointer=checkpointer)


customer_support_graph = build_workflow()
