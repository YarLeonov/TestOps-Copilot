from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    name: str = Field(..., description="Название проекта")
    description: Optional[str] = Field(default=None, description="Краткое описание проекта")


class ProjectCreate(ProjectBase):
    """Данные для создания проекта."""
    pass


class ProjectRead(ProjectBase):
    id: str = Field(..., description="Идентификатор проекта")
