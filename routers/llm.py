from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import DBSessionDep
from models import Conversation, Message
from repositories.messages import MessageRepository
from services.llm import LLMService
from services.conversations import ConversationService
from schemas import LLMConversationRequest, LLMTextRequest, LLMConversationResponse, LLMTextResponse

router = APIRouter(prefix="/llm")
llm_service = LLMService()

async def get_conversation(
    conversation_id: int, session: DBSessionDep
) -> Conversation:
    conversation = await ConversationService(session).get(conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )
    return conversation

GetConversationDep = Annotated[Conversation, Depends(get_conversation)]

async def store_message(
    prompt_content: str,
    response_content: str,
    conversation_id: int,
    session: AsyncSession,
) -> None:
    """Store message in the database"""
    try:
        message = Message(
            conversation_id=conversation_id,
            prompt_content=prompt_content,
            response_content=response_content,
            prompt_tokens=len(prompt_content.split()),  # Simple token estimation
            response_tokens=len(response_content.split()),
            total_tokens=len(prompt_content.split()) + len(response_content.split()),
            is_success=True,
            status_code=200
        )
        await MessageRepository(session).create(message)
    except Exception as e:
        print(f"Error storing message: {e}")

@router.post("/conversations", response_model=LLMConversationResponse)
async def create_conversation_with_llm(
    request: LLMConversationRequest,
    session: DBSessionDep,
) -> LLMConversationResponse:
    """Create a new conversation with AI-generated title"""
    conversation = await llm_service.create_conversation_with_title(request.prompt, session)
    return LLMConversationResponse(
        conversation_id=conversation.id,
        title=conversation.title,
        message="Conversation created successfully"
    )

async def stream_generator(prompt: str, conversation_id: int, session: AsyncSession):
    """Generator for streaming response"""
    response_content = ""
    
    async for chunk in llm_service.stream_response(prompt, conversation_id):
        response_content += chunk
        yield chunk
    
    # Store message after streaming is complete
    await store_message(prompt, response_content, conversation_id, session)

@router.post("/text/generate/stream")
async def stream_llm_controller(
    request: LLMTextRequest,
    session: DBSessionDep,
) -> StreamingResponse:
    """Stream LLM response and store message in background"""
    # Verify conversation exists
    conversation = await get_conversation(request.conversation_id, session)
    
    return StreamingResponse(
        stream_generator(request.prompt, request.conversation_id, session),
        media_type="text/plain",
        headers={"Content-Type": "text/plain; charset=utf-8"}
    )

@router.post("/text/generate", response_model=LLMTextResponse)
async def generate_text_controller(
    request: LLMTextRequest,
    session: DBSessionDep,
) -> LLMTextResponse:
    """Generate text response and store message"""
    conversation = await get_conversation(request.conversation_id, session)
    
    response_content = ""
    async for chunk in llm_service.stream_response(request.prompt, request.conversation_id):
        response_content += chunk
    
    await store_message(request.prompt, response_content, conversation.id, session)
    
    return LLMTextResponse(
        response=response_content,
        conversation_id=request.conversation_id,
        prompt=request.prompt
    ) 