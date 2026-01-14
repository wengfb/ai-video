import uuid
import enum
from sqlalchemy import String, Text, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.models.base import BaseModel


class EpisodeStatus(str, enum.Enum):
    DRAFT = "draft"
    SCRIPTING = "scripting"
    STORYBOARDING = "storyboarding"
    GENERATING = "generating"
    COMPLETED = "completed"


class Episode(BaseModel):
    """分集/章节"""
    __tablename__ = "episodes"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
    )
    title: Mapped[str] = mapped_column(String(255))
    synopsis: Mapped[str | None] = mapped_column(Text)
    order: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[EpisodeStatus] = mapped_column(
        Enum(EpisodeStatus),
        default=EpisodeStatus.DRAFT,
    )

    project: Mapped["Project"] = relationship(back_populates="episodes")
    script: Mapped["Script | None"] = relationship(
        back_populates="episode",
        uselist=False,
    )
    storyboards: Mapped[list["Storyboard"]] = relationship(
        back_populates="episode",
    )
