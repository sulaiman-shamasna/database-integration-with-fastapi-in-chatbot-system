from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from services.conversations import ConversationService
from models import Conversation, Message
from schemas import ConversationCreate, ConversationUpdate, ConversationOut, MessageOut
from database import DBSessionDep

router = APIRouter(prefix="/conversations")


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


@router.get("/{conversation_id}/messages", response_model=List[MessageOut])
async def list_conversation_messages_controller(
    conversation: GetConversationDep,
    session: DBSessionDep,
):
    messages = await ConversationService(session).list_messages(conversation.id)
    return messages  # FastAPI will use the response_model to serialize


@router.get("")
async def list_conversations_controller(
    session: DBSessionDep, skip: int = 0, take: int = 100
) -> List[ConversationOut]:
    conversations = await ConversationService(session).list(skip, take)
    return [ConversationOut.model_validate(c) for c in conversations]


@router.get("/{conversation_id}")
async def get_conversation_controller(
    conversation: GetConversationDep,
) -> ConversationOut:
    return ConversationOut.model_validate(conversation)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_conversation_controller(
    conversation: ConversationCreate, session: DBSessionDep
) -> ConversationOut:
    new_conversation = await ConversationService(session).create(
        conversation
    )
    return ConversationOut.model_validate(new_conversation)


@router.put("/{conversation_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_conversation_controller(
    conversation: GetConversationDep,
    updated_conversation: ConversationUpdate,
    session: DBSessionDep,
) -> ConversationOut:
    updated_conversation = await ConversationService(session).update(
        conversation.id, updated_conversation
    )
    return ConversationOut.model_validate(updated_conversation)


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation_controller(
    conversation: GetConversationDep, session: DBSessionDep
) -> None:
    await ConversationService(session).delete(conversation.id)