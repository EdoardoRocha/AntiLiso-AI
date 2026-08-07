from fastapi import APIRouter
from models.transactions_model import AntilisoPost, AntilisoResponse
from ai.agent import antiliso_agent
from datetime import datetime

now = datetime.now()
router = APIRouter(prefix="/antiliso", tags=["antiliso"])


@router.post("/invoke", response_model=AntilisoResponse, )
async def invoke_antiliso(body: AntilisoPost) -> AntilisoResponse:
    try:
        config = {"configurable": {"thread_id": str(body.conversation_id)}}
        agent_invoke = await antiliso_agent.ainvoke({"messages": [
            {"role": "user", "content": f"{body.text} + ID Do usuário: {body.user_id} + Data de agora: {now}"}]},
            config)
        agent_response = agent_invoke['messages'][-1].text
        return AntilisoResponse(text=agent_response)
    except Exception as e:
        return AntilisoResponse(text=f"Erro inesperado {e}")
