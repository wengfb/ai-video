import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from app.models.base import BaseModel


class WorldSetting(BaseModel):
    """世界观设定"""
    __tablename__ = "world_settings"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
    )
    content: Mapped[str | None] = mapped_column(Text)
    keywords: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=list,
    )

    project: Mapped["Project"] = relationship(
        back_populates="world_setting",
    )
