from sqlalchemy import (
    String, Text, ForeignKey, Boolean, Table, Column,
    Integer, DateTime, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Enum

from app.models.base import Base
from app.models.enums import MessageType

group_members = Table(
    'group_members',
    Base.metadata,
    Column(
        'user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'),
        primary_key=True
    ),
    Column(
        'group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'),
        primary_key=True
    ),
    Column('joined_at', DateTime(timezone=True), server_default=func.now()),
    Column('is_admin', Boolean, default=False)
)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(255), nullable=False)
    creator_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'), nullable=False
    )
    is_private: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    # Relationships
    creator: Mapped["User"] = relationship(
        "User", back_populates="created_groups"
    )
    members: Mapped[list["User"]] = relationship(
        "User", secondary=group_members, back_populates="groups"
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="group", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey('groups.id', ondelete='CASCADE'), nullable=False
    )
    sender_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    receiver_id = Column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True
    )

    content: Mapped[str] = mapped_column(Text, nullable=False)
    message_type = Column(Enum(MessageType), default=MessageType.TEXT)

    # Relationships
    group: Mapped["Group"] = relationship("Group", back_populates="messages")
    sender: Mapped["User"] = relationship(
        "User",
        back_populates="sent_messages",
        foreign_keys=[sender_id]
    )
    receiver: Mapped["User"] = relationship(
        "User",
        foreign_keys=[receiver_id]
    )
    media: Mapped[list["MessageMedia"]] = relationship(
        "MessageMedia", back_populates="message", cascade="all, delete-orphan"
    )


class MessageMedia(Base):
    __tablename__ = "message_media"

    id = Column(Integer, primary_key=True, index=True)
    message_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(
            'messages.id', ondelete='CASCADE'
        ), nullable=False, index=True
    )
    media_type: Mapped[MessageType] = mapped_column(
        Enum(MessageType), nullable=False
    )

    s3_key: Mapped[str] = mapped_column(String(512), nullable=False)
    s3_url: Mapped[str] = mapped_column(String(1024), nullable=False)

    # Метаданные
    file_size: Mapped[int] = mapped_column(nullable=False)
    duration: Mapped[float] = mapped_column(nullable=True)
    mime_type: Mapped[str] = mapped_column(String(50), default="image/jpeg")
    width: Mapped[int] = mapped_column(Integer, nullable=False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    original_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationship
    message: Mapped["Message"] = relationship(
        "Message", back_populates="media"
    )
