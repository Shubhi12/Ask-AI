import uuid
from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse
from app.services.helpers import get_conversation, store_conversations, reset_conversations
from app.services.llm_services import LLMServices

router = APIRouter()
llm_services = LLMServices()

@router.post("/", tags=["chat"])
def chat(request:ChatRequest):
    try:
        conversation_id = request.conversation_id
        if conversation_id is None:
            conversation_id = str(uuid.uuid4())
        conversation = dict()
        conversation["role"] = "user"
        conversation["content"] = request.message
        conversations = store_conversations(conversation,conversation_id)
        response = llm_services.call_llm_model(messages=conversations)
        print(response)
        response_text = response
        conversation_response = {"role": "assistant", "content": response_text}
        store_conversations(conversation_response,conversation_id)
        return ChatResponse(conversation_id=conversation_id,message=response_text)
    except Exception as e:
        print(e)
        return {"error": str(e),
                "status": "error",
                "http_code": 500}

@router.post("/reset", tags=["chat"])
def reset_chat(request:ChatRequest):
    try:
        reset_conversations(request.conversation_id)
        return ChatResponse(conversation_id=request.conversation_id,message="Chat reset successfully")
    except Exception as e:
        print(e)
        return {"error": str(e),
                "status": "error",
                "http_code": 500}