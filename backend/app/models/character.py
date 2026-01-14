import uuid
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from app.models.base import BaseModel


class Character(BaseModel):
    """角色模型"""
    __tablename__ = "characters"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    appearance: Mapped[str | None] = mapped_column(Text)
    personality: Mapped[str | None] = mapped_column(Text)
    reference_assets: Mapped[list[str]] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        default=list,
    )
    lora_model_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    consistency_config: Mapped[dict] = mapped_column(JSONB, default=dict)

    project: Mapped["Project"] = relationship(back_populates="characters")
