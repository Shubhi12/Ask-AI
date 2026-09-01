from fastapi import APIRouter
from app.schemas import AskRequest
from app.models.knowledge_base import KnowledgeBase
from app.services.prompts import COMPANY_POLICY_PROMPT, SYSTEM_PROMPT
from app.services.llm_services import LLMServices

router = APIRouter()
llm_services = LLMServices()

@router.post("/ask",tags=["rag"])
def ask(request:AskRequest):
    try:
        query_embedding = llm_services.embed_text([request.text])
        context = KnowledgeBase.search_vector_similarity(query_embedding[0],k=3)
        print("Context: ",context)
        context_list = []
        for item in context:
            context_list.append(item['content'])
        context = '\n\n'.join(context_list)
        prompt = COMPANY_POLICY_PROMPT.format(
            context=context,
            question=request.text
        )
        response = llm_services.call_llm_model(messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user","content": prompt}
        ])
        return {"answer":response,"context":context}
    except Exception as e:
        print(e)
        return {"error": str(e),
                "status": "error",
                "http_code": 500}
