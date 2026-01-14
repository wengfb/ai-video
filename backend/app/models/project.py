import uuid
import enum
from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from app.models.base import BaseModel


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Project(BaseModel):
    """项目模型"""
    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus),
        default=ProjectStatus.DRAFT,
    )
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)

    # 关联
    world_setting: Mapped["WorldSetting | None"] = relationship(
        back_populates="project",
        uselist=False,
    )
    characters: Mapped[list["Character"]] = relationship(
        back_populates="project",
    )
    scenes: Mapped[list["Scene"]] = relationship(
        back_populates="project",
    )
    episodes: Mapped[list["Episode"]] = relationship(
        back_populates="project",
    )
