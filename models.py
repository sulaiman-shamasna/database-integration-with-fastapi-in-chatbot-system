from datetime import datetime, UTC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Conversation(Base):
    __tablename__ = 'conversations'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC), onupdate=datetime.now(UTC))
    model_type: Mapped[str] = mapped_column(nullable=False)
    messages: Mapped[list['Message']] = relationship(back_populates='conversation')

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(primary_key=True)
    conversation_id: Mapped[int] = mapped_column(ForeignKey('conversations.id'), nullable=False) # TODO: Add cascade delete
    prompt_content: Mapped[str] = mapped_column(nullable=False)
    response_content: Mapped[str] = mapped_column(nullable=False)
    prompt_tokens: Mapped[int] = mapped_column(nullable=False)
    response_tokens: Mapped[int] = mapped_column(nullable=False)
    total_tokens: Mapped[int | None] = mapped_column(nullable=False)
    is_success: Mapped[bool | None] = mapped_column(nullable=False, default=True)
    status_code: Mapped[int | None] = mapped_column(nullable=False, default=200)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC), onupdate=datetime.now(UTC))
    conversation: Mapped[Conversation] = relationship("Conversation", back_populates='messages')