import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from app.models.base import BaseModel


class Scene(BaseModel):
    """场景模型"""
    __tablename__ = "scenes"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    reference_assets: Mapped[list[str]] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        default=list,
    )
    style_config: Mapped[dict] = mapped_column(JSONB, default=dict)

    project: Mapped["Project"] = relationship(back_populates="scenes")
