
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from uuid import UUID

from langchain_core.messages import HumanMessage

from app.graph.workflow import customer_support_graph


router = APIRouter()


# ==========================================
# CHAT REQUEST
# ==========================================

class ChatRequest(BaseModel):
    message: str
    session_id: UUID


# ==========================================
# CHAT ENDPOINT
# ==========================================

@router.post("/chat")
def chat(request: ChatRequest):

    # Identify the customer's conversation
    config = {
        "configurable": {
            "thread_id": str(request.session_id)
        }
    }

    try:

        # Send the new customer message to LangGraph
        result = customer_support_graph.invoke(
            {
                "messages": [
                    HumanMessage(content=request.message)
                ]
            },
            config=config
        )

        # ==================================
        # Get the latest assistant response
        # ==================================

        answer = None

        for msg in reversed(result["messages"]):

            if getattr(msg, "type", None) == "ai":
                answer = msg.content
                break

        if answer is None:
            raise ValueError(
                "No assistant response was generated."
            )

        # ==================================
        # Determine workflow status
        # ==================================

        next_action = result.get("next_action")

        # Case 1: Safety concern
        if next_action == "safety_escalation":

            status = "safety_escalation"

        # Case 2: Safety clarification
        elif next_action == "safety_clarification":

            status = "safety_clarification"

        # Case 3: Information collection incomplete
        elif not result.get("is_complete", False):

            status = "incomplete"

        # Case 4: Information collection complete
        else:

            answer = (
                "Thank you! I have collected enough information "
                "to begin processing your request."
            )

            status = "complete"

        # ==================================
        # Return API response
        # ==================================

        return {
            "answer": answer,
            "status": status,
            "session_id": str(request.session_id)
        }

    except Exception as error:

        print(f"Chat workflow error: {error}")

        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your request."
        )
