
from typing import TypedDict, Optional, List, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage


class CustomerSupportState(TypedDict):

    # Conversation history
    messages: Annotated[list[AnyMessage], add_messages]

    # Language
    language: Optional[str]

    # Customer intent
    customer_intent: Optional[str]

    # Product information
    product_type: Optional[str]
    product_model: Optional[str]
    symptoms: List[str]
    error_code: Optional[str]
    conflicts: List[str]

    # Information validation
    missing_fields: List[str]
    is_complete: bool

    # Agent 2
    follow_up_question: Optional[str]

    # Safety
    safety_classification: Optional[str]
    safety_reason: Optional[str]

    # Workflow
    next_action: Optional[str]
