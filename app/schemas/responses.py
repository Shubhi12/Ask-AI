from pydantic import BaseModel, Field
from app.enums import Priority, IssueCategory, SummarizeStyle, Tone, Audience

class ExtractResponse(BaseModel):
    customer: str = Field(...,min_length=1)
    company: str = Field(...,min_length=1)
    issue: str = Field(...,min_length=1)
    priority: Priority

class ClassifyResponse(BaseModel):
    category: IssueCategory
    confidence: float = Field(...,ge=0,le=1)

class SummarizeResponse(BaseModel):
    summary: str = Field(...,min_length=1)
    style: SummarizeStyle

class GenerateResponse(BaseModel):
    content: str = Field(...,min_length=1)
    metadata: dict = Field(default={"topic":str,"audience":Audience,"tone":Tone})

class ChatResponse(BaseModel):
    conversation_id: str
    message: str = Field(...,min_length=1)