import uuid
import enum
from sqlalchemy import String, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

from app.models.base import BaseModel


class WorkflowCategory(str, enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    ANIMATION = "animation"


class ComfyWorkflow(BaseModel):
    """ComfyUI 工作流模板"""
    __tablename__ = "comfy_workflows"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    category: Mapped[WorkflowCategory] = mapped_column(Enum(WorkflowCategory))
    workflow_json: Mapped[dict] = mapped_column(JSONB, default=dict)
    input_schema: Mapped[dict] = mapped_column(JSONB, default=dict)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
