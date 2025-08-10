
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional

class ConversationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    model_type: str

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(ConversationBase):
    pass

class ConversationOut(ConversationBase):
    id: int
    created_at: datetime
    updated_at: datetime

class MessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    conversation_id: int
    prompt_content: str
    response_content: str
    prompt_tokens: int
    response_tokens: int
    total_tokens: Optional[int]
    is_success: Optional[bool]
    status_code: Optional[int]
    created_at: datetime
    updated_at: datetime

class LLMConversationRequest(BaseModel):
    prompt: str

class LLMTextRequest(BaseModel):
    prompt: str
    conversation_id: int

class LLMConversationResponse(BaseModel):
    conversation_id: int
    title: str
    message: str

class LLMTextResponse(BaseModel):
    response: str
    conversation_id: int
    prompt: str