import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Date, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import BaseModel


if TYPE_CHECKING:
    from . import UserModel


class MoodEntry(BaseModel):
    __tablename__ = "mood_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid.uuid4()), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    mood: Mapped[str] = mapped_column(String(50), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)

    user: Mapped["UserModel"] = relationship(
        back_populates="mood_entries",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<MoodEntryModel(id={self.id}, uuid={self.uuid}m mood={self.mood}, date={self.date})>"
