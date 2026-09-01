import json
from fastapi import APIRouter
from app.schemas import ExtractRequest, ExtractResponse
from app.services.prompts import EXTRACT_PROMPT
from app.services.llm_services import LLMServices

router = APIRouter()
llm_services = LLMServices()

@router.post("/", tags=["extract"])
def extract(request: ExtractRequest):
    try:
        response = llm_services.call_llm_model(messages=[
                {
                    "role": "user",
                    "content": EXTRACT_PROMPT.format(
                        text=request.text
                    )
                }
                ])
        response = json.loads(response)
        return ExtractResponse(customer=response.get("customer"),company=response.get("company"),issue=response.get("issue"),priority=response.get("priority"))
    except Exception as e:
        print(e)
        return {"error": str(e),
                "status": "error",
                "http_code": 500}