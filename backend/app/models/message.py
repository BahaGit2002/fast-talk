from sqlalchemy import (
    Text, ForeignKey, DateTime, func, Index, String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM

from app.models.base import Base
from app.models.enums import MessageType


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    chat_id: Mapped[int | None] = mapped_column(
        ForeignKey('chats.id', ondelete='CASCADE'), nullable=True, index=True
    )
    group_id: Mapped[int | None] = mapped_column(
        ForeignKey('groups.id', ondelete='CASCADE'), nullable=True, index=True
    )

    sender_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )

    message_type: Mapped[MessageType] = mapped_column(
        ENUM(MessageType, create_type=True), nullable=False
    )

    content: Mapped[str | None] = mapped_column(Text, nullable=True)

    is_read: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # Relationships
    chat: Mapped["Chat | None"] = relationship("Chat", back_populates="messages")
    group: Mapped["Group | None"] = relationship("Group", back_populates="messages")
    sender: Mapped["User"] = relationship("User", back_populates="messages_sent")

    media: Mapped[list["MessageMedia"]] = relationship(
        "MessageMedia", back_populates="message", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_chat_id', 'chat_id', postgresql_where=(chat_id.is_not(None))),
        Index('idx_group_id', 'group_id', postgresql_where=(group_id.is_not(None))),
    )


class MessageMedia(Base):
    __tablename__ = "message_media"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    message_id: Mapped[int] = mapped_column(
        ForeignKey('messages.id', ondelete='CASCADE'), nullable=False, index=True
    )

    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    s3_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    width: Mapped[int | None] = mapped_column(nullable=True)
    height: Mapped[int | None] = mapped_column(nullable=True)
    duration: Mapped[float | None] = mapped_column(nullable=True)

    original_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship
    message: Mapped["Message"] = relationship("Message", back_populates="media")
