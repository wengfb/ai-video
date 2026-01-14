import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Text, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

from app.models.base import BaseModel


class TaskType(str, enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    COMPOSITE = "composite"


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRY_PENDING = "retry_pending"
    MANUAL_REVIEW = "manual_review"


class GenerationTask(BaseModel):
    """生成任务"""
    __tablename__ = "generation_tasks"

    dag_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("task_dags.id", ondelete="CASCADE"),
        nullable=True,
    )
    storyboard_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("storyboards.id", ondelete="SET NULL"),
        nullable=True,
    )
    workflow_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("comfy_workflows.id"),
    )
    task_type: Mapped[TaskType] = mapped_column(Enum(TaskType))
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
    )
    priority: Mapped[int] = mapped_column(Integer, default=50)
    input_params: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_assets: Mapped[list[str]] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        default=list,
    )
    error_message: Mapped[str | None] = mapped_column(Text)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    retry_delay: Mapped[int] = mapped_column(Integer, default=5)
    timeout: Mapped[int] = mapped_column(Integer, default=600)
    resource_requirements: Mapped[dict] = mapped_column(JSONB, default=dict)
    version: Mapped[int] = mapped_column(Integer, default=1)
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    parent_task_ids: Mapped[list[str]] = mapped_column(
        ARRAY(UUID(as_uuid=True)),
        default=list,
    )
