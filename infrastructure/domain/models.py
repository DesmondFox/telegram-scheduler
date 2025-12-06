from datetime import datetime
import enum
from sqlalchemy import BigInteger, Boolean, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from infrastructure.domain.base import BaseEntity


class UserModel(BaseEntity):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str | None] = mapped_column(String(32), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    first_name: Mapped[str | None] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))
    language_code: Mapped[str | None] = mapped_column(String(10))

class PlatformEnum(str, enum.Enum):
    TELEGRAM = "telegram"
    DISCORD = "discord"

class ChannelModel(BaseEntity):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    platform: Mapped[PlatformEnum] = mapped_column(Enum(PlatformEnum))
    channel_id: Mapped[str] = mapped_column(String(255))
    target_id: Mapped[str] = mapped_column(String(1024)) # channel id, webhook url, etc.
    title: Mapped[str | None] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="channels")