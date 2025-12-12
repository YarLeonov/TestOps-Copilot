from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Requirement:
    """Внутренняя модель требования."""

    id: str
    title: str
    description: str
    area: Optional[str] = None
    priority: str = "medium"
