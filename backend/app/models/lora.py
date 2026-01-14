import uuid
import enum
from sqlalchemy import String, Text, Integer, Float, BigInteger, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from app.models.base import BaseModel


class LoraType(str, enum.Enum):
    CHARACTER = "character"
    STYLE = "style"
    CONCEPT = "concept"
    OBJECT = "object"


class LoraStatus(str, enum.Enum):
    PENDING = "pending"
    TRAINING = "training"
    READY = "ready"
    FAILED = "failed"
    ARCHIVED = "archived"


class LoraAsset(BaseModel):
    """LoRA 资产"""
    __tablename__ = "lora_assets"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    type: Mapped[LoraType] = mapped_column(Enum(LoraType))
    status: Mapped[LoraStatus] = mapped_column(
        Enum(LoraStatus),
        default=LoraStatus.PENDING,
    )
    base_model: Mapped[str] = mapped_column(String(100))
    base_model_hash: Mapped[str | None] = mapped_column(String(64))
    trigger_words: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    recommended_weight: Mapped[float] = mapped_column(Float, default=0.8)
    weight_range: Mapped[dict] = mapped_column(
        JSONB,
        default=lambda: {"min": 0.3, "max": 1.0},
    )
    file_path: Mapped[str | None] = mapped_column(String(500))
    file_size: Mapped[int | None] = mapped_column(BigInteger)
    file_hash: Mapped[str | None] = mapped_column(String(64))
    preview_images: Mapped[list[str]] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        default=list,
    )
    training_task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    project_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_by: Mapped[str | None] = mapped_column(String(100))
