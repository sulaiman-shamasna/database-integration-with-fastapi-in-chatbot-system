from models import Message
from repositories.conversations import ConversationRepository
from sqlalchemy import select
from typing import List


class ConversationService(ConversationRepository):
    async def list_messages(self, conversation_id: int) -> List[Message]:
        result = await self.session.execute(
            select(Message).where(Message.conversation_id == conversation_id)
        )
        return [m for m in result.scalars().all()]
