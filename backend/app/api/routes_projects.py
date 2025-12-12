from __future__ import annotations

from typing import Dict, List
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.schemas.project import ProjectCreate, ProjectRead

router = APIRouter()

# Простое in-memory хранилище под демо
_PROJECTS: Dict[str, ProjectRead] = {}


@router.get("", response_model=List[ProjectRead])
async def list_projects() -> List[ProjectRead]:
    return list(_PROJECTS.values())


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate) -> ProjectRead:
    project_id = str(uuid4())
    project = ProjectRead(id=project_id, **payload.model_dump())
    _PROJECTS[project_id] = project
    return project


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: str) -> ProjectRead:
    project = _PROJECTS.get(project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project
