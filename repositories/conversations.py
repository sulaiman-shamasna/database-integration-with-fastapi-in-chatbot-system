from models import Conversation
from repositories.interfaces import Repository
from schemas import ConversationCreate, ConversationUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Union


class ConversationRepository(Repository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, skip: int, take: int) -> List[Conversation]:
        result = await self.session.execute(
            select(Conversation).offset(skip).limit(take)
        )
        return [r for r in result.scalars().all()]

    async def get(self, conversation_id: int) -> Optional[Conversation]:
        result = await self.session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalars().first()

    async def create(self, conversation: Union[ConversationCreate, Conversation]) -> Conversation:
        if isinstance(conversation, ConversationCreate):
            new_conversation = Conversation(**conversation.model_dump())
        else:
            new_conversation = conversation
            
        self.session.add(new_conversation)
        await self.session.commit()
        await self.session.refresh(new_conversation)
        return new_conversation

    async def update(
        self, conversation_id: int, updated_conversation: ConversationUpdate
    ) -> Optional[Conversation]:
        conversation = await self.get(conversation_id)
        if not conversation:
            return None
        for key, value in updated_conversation.model_dump().items():
            setattr(conversation, key, value)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def delete(self, conversation_id: int) -> None:
        conversation = await self.get(conversation_id)
        if not conversation:
            return
        await self.session.delete(conversation)
        await self.session.commit()