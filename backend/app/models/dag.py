import uuid
import enum
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.models.base import BaseModel


class DAGStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TriggerType(str, enum.Enum):
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    API = "api"


class TaskDAG(BaseModel):
    """任务有向无环图"""
    __tablename__ = "task_dags"

    name: Mapped[str] = mapped_column(String(255))
    episode_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("episodes.id", ondelete="SET NULL"),
        nullable=True,
    )
    status: Mapped[DAGStatus] = mapped_column(
        Enum(DAGStatus),
        default=DAGStatus.PENDING,
    )
    trigger_type: Mapped[TriggerType] = mapped_column(
        Enum(TriggerType),
        default=TriggerType.MANUAL,
    )
    created_by: Mapped[str | None] = mapped_column(String(100))
    total_tasks: Mapped[int] = mapped_column(Integer, default=0)
    completed_tasks: Mapped[int] = mapped_column(Integer, default=0)
    failed_tasks: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
