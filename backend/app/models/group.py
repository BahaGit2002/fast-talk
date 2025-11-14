from typing import Optional
from sqlalchemy import String, Text, ForeignKey, Boolean, Table, Column, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

group_members = Table(
    'group_members',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True),
    Column('joined_at', DateTime(timezone=True), server_default=func.now()),
    Column('is_admin', Boolean, default=False)
)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avatar_url: Mapped[str] = mapped_column(String(255), nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=False)
    is_private: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # Relationships
    creator: Mapped["User"] = relationship("User", back_populates="created_groups")
    members: Mapped[list["User"]] = relationship(
        "User", secondary=group_members, back_populates="groups"
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="group", cascade="all, delete-orphan"
    )
