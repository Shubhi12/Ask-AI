from fastapi import APIRouter
from app.schemas import SummarizeRequest, SummarizeResponse
from app.services.prompts import SUMMARIZE_PROMPT
from app.services.llm_services import LLMServices

router = APIRouter()
llm_services = LLMServices()

@router.post("/", tags=["summarize"])
def summarize(request: SummarizeRequest):
    prompt = SUMMARIZE_PROMPT.format(
        text=request.text,
        max_length=request.max_length,
        style=request.style.value
    )
    try:
        response = llm_services.call_llm_model(messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                    ])
        return SummarizeResponse(summary=response,style=request.style.value)
    except TimeoutError:
        return {"error": "Request timed out",
                "status": "error"
            }
    except Exception as e:
        return {"error": str(e),
                "status": "error"}