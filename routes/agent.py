from fastapi import APIRouter, Depends
from schemas import AIRequest, AIResponse
from services.agent_service import agent
from dependencies import get_current_user
from services.agent_service import AgentContext

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("", response_model=AIResponse)
def chat(
    request: AIRequest,
    user = Depends(get_current_user)
):

    result = agent.invoke(
        {"messages": [{"role": "user", "content": request.message}]},
        context= AgentContext(user_id = user.user_id)
        )

    return {
        "response": result["messages"][-1].content
    }