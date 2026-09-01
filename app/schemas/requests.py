from typing_extensions import Optional
from pydantic import BaseModel, Field
from app.enums import SummarizeStyle, Audience, Tone, Length


class ClientRequest(BaseModel):
    text: str = Field(...,min_length=1)

class SummarizeRequest(BaseModel):
    text: str = Field(...,min_length=1)
    max_length: int = Field(...,ge=1)
    style: SummarizeStyle

class ExtractRequest(ClientRequest):
    pass

class ClassifyRequest(ClientRequest):
    pass

class GenerateRequest(BaseModel):
    topic: str
    audience: Audience
    tone: Tone
    length: Length

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str = Field(...,min_length=1)

class ToolsRequest(ClientRequest):
    pass

class ProcessDocumentRequest(ClientRequest):
    pass

class AskRequest(ClientRequest):
    pass

from typing import List

class UploadRequest(BaseModel):
    file_name: Optional[str] = Field(None, min_length=1)
    file_names: Optional[List[str]] = Field(None)
    file_path: Optional[str] = Field(None, min_length=1)
    file_paths: Optional[List[str]] = Field(None)
    user_name: Optional[str] = Field("default_user", min_length=1)




class UserLoginRequest(BaseModel):
    username: Optional[str] = Field(None,min_length=1)
    email: Optional[str] = Field(None,min_length=1)
    password: str = Field(...,min_length=1)

class UserRegisterRequest(BaseModel):
    username: str = Field(...,min_length=1)
    email: str = Field(...,min_length=1)
    password: str = Field(...,min_length=1)
    company_name: str = Field(...,min_length=1)
    description: Optional[str] = None
    
