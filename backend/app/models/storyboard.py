import uuid
from sqlalchemy import String, Text, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from app.models.base import BaseModel


class Storyboard(BaseModel):
    """分镜"""
    __tablename__ = "storyboards"

    episode_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("episodes.id", ondelete="CASCADE"),
    )
    scene_number: Mapped[int] = mapped_column(Integer)
    description: Mapped[str | None] = mapped_column(Text)
    duration: Mapped[float] = mapped_column(Float, default=3.0)
    camera_movement: Mapped[str | None] = mapped_column(String(100))
    characters: Mapped[list[str]] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        default=list,
    )
    scene_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scenes.id", ondelete="SET NULL"),
        nullable=True,
    )
    dialogue: Mapped[str | None] = mapped_column(Text)
    notes: Mapped[str | None] = mapped_column(Text)
    thumbnail_asset_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    generation_config: Mapped[dict] = mapped_column(JSONB, default=dict)

    episode: Mapped["Episode"] = relationship(back_populates="storyboards")
