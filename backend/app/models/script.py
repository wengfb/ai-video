import uuid
from sqlalchemy import Text, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.models.base import BaseModel


class Script(BaseModel):
    """剧本"""
    __tablename__ = "scripts"

    episode_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("episodes.id", ondelete="CASCADE"),
        unique=True,
    )
    content: Mapped[str | None] = mapped_column(Text)
    structured_content: Mapped[dict] = mapped_column(JSONB, default=dict)
    version: Mapped[int] = mapped_column(Integer, default=1)

    episode: Mapped["Episode"] = relationship(back_populates="script")
