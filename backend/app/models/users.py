from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_online: Mapped[bool] = mapped_column(Boolean, default=False)
    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    avatar: Mapped[Optional["UserAvatar"]] = relationship(
        "UserAvatar", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    created_groups: Mapped[list["Group"]] = relationship("Group", back_populates="creator")
    groups: Mapped[list["Group"]] = relationship(
        "Group", secondary="group_members", back_populates="members"
    )
    chats_as_user1: Mapped[list["Chat"]] = relationship(
        "Chat", back_populates="user1", foreign_keys="Chat.user1_id"
    )
    chats_as_user2: Mapped[list["Chat"]] = relationship(
        "Chat", back_populates="user2", foreign_keys="Chat.user2_id"
    )
    messages_sent: Mapped[list["Message"]] = relationship(
        "Message", back_populates="sender"
    )
