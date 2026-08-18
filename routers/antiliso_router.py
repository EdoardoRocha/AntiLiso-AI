from fastapi import APIRouter
from models.transactions_model import AntilisoPost, AntilisoResponse
from ai.agent import antiliso_agent
from datetime import date
from langchain_core.messages import HumanMessage
from helpers.image_encode import image_to_base64

today = date.today()
router = APIRouter(prefix="/antiliso", tags=["antiliso"])


@router.post("/invoke", response_model=AntilisoResponse, )
async def invoke_antiliso(body: AntilisoPost) -> AntilisoResponse:
    try:
        configuracao = {
            "configurable": {
                "user_id": body.user_id,
                "thread_id": str(body.conversation_id)
            },
            "metadata": {
                "source": "antiliso",
            }
        }

        user_content = []
        if body.text:
            user_content.append({"type": "text", "text": f"Mensagem do usuário: {body.text}. data de hoje(Apenas para referência): {today}"})
        img_url = getattr(body, "img_url", None)
        if img_url and img_url != "http://localhost:3000/":
            image_data, mime_type = await image_to_base64(img_url)

            user_content.append({
                "type": "image",
                "source_type": "base64",
                "data": image_data,
                "mime_type": mime_type,
            })

        inputs = {"messages": [HumanMessage(content=user_content)]}
        agent_invoke = await antiliso_agent.ainvoke(input=inputs, config=configuracao)
        agent_response = agent_invoke['messages'][-1].content
        return AntilisoResponse(text=agent_response)
    except Exception as e:
        return AntilisoResponse(text=f"Erro inesperado {e}")
