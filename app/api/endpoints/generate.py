import json
from fastapi import APIRouter
from app.schemas import GenerateRequest, GenerateResponse
from app.services.prompts import GENERATE_PROMPT
from app.services.llm_services import LLMServices
from app.services.helpers import get_role, get_domain

router = APIRouter()
llm_services = LLMServices()

@router.post("/", tags=["generate"])
def generate(request: GenerateRequest):
    try:
        response = llm_services.call_llm_model(messages=[
                {
                    "role": "user",
                    "content": GENERATE_PROMPT.format(
                        role=get_role(request.tone.value,request.audience.value),
                        domain=get_domain(request.audience.value),
                        topic=request.topic,
                        audience=request.audience.value,
                        tone=request.tone.value, 
                        length=request.length.value
                    )
                }
                ])
        return GenerateResponse(content=response,metadata={"topic":request.topic,"audience":request.audience.value,"tone":request.tone.value})
    except Exception as e:
        print(e)
        return {"error": str(e),
                "status": "error",
                "http_code": 500}