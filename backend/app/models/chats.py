from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user1_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user2_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    user1: Mapped["User"] = relationship("User", foreign_keys=[user1_id], back_populates="chats_as_user1")
    user2: Mapped["User"] = relationship("User", foreign_keys=[user2_id], back_populates="chats_as_user2")
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint('user1_id', 'user2_id', name='unique_chat_users'),
        Index('idx_user1_user2', 'user1_id', 'user2_id'),
        Index('idx_user2_user1', 'user2_id', 'user1_id'),
    )
