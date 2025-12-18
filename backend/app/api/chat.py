from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.agent.yarden import YardenAgent
import uuid

router = APIRouter()

# Lazy initialization
_agent = None


def get_agent():
    global _agent
    if _agent is None:
        _agent = YardenAgent()
    return _agent


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to Yarden and get a response."""
    try:
        session_id = request.session_id or str(uuid.uuid4())
        agent = get_agent()

        response = await agent.chat(
            user_id=request.user_id,
            message=request.message,
            session_id=session_id
        )

        return ChatResponse(
            response=response,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
