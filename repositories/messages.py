from models import Message
from repositories.interfaces import Repository
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional


class MessageRepository(Repository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list(self, skip: int = 0, take: int = 100) -> List[Message]:
        result = await self.session.execute(
            select(Message).offset(skip).limit(take)
        )
        return [r for r in result.scalars().all()]

    async def get(self, message_id: int) -> Optional[Message]:
        result = await self.session.execute(
            select(Message).where(Message.id == message_id)
        )
        return result.scalars().first()

    async def create(self, message: Message) -> Message:
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def update(self, message_id: int, updated_message: Message) -> Optional[Message]:
        message = await self.get(message_id)
        if not message:
            return None
        for key, value in updated_message.__dict__.items():
            if not key.startswith('_'):
                setattr(message, key, value)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def delete(self, message_id: int) -> None:
        message = await self.get(message_id)
        if not message:
            return
        await self.session.delete(message)
        await self.session.commit()

    async def list_by_conversation(self, conversation_id: int) -> List[Message]:
        result = await self.session.execute(
            select(Message).where(Message.conversation_id == conversation_id)
        )
        return [r for r in result.scalars().all()] 