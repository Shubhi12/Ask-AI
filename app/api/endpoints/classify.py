import json
from fastapi import APIRouter
from app.schemas import ClassifyRequest, ClassifyResponse
from app.services.prompts import CLASSIFY_PROMPT
from app.services.llm_services import LLMServices

router = APIRouter()
llm_services = LLMServices()

@router.post("/", tags=["classify"])
def classify(request: ClassifyRequest):
    try:
        response = llm_services.call_llm_model(messages=[
            {
                "role": "user",
                "content": CLASSIFY_PROMPT.format(
                    text=request.text
                )
            }
            ])
        response = json.loads(response)
        return ClassifyResponse(category=response.get("category"),confidence=response.get("confidence"))
    except TimeoutError:
        return {"error": "Request timed out",
                "status": "error"}
    except Exception as e:
        return {"error": str(e),
                "status": "error"}
