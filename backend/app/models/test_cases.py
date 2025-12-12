from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TestCaseStep:
    order: int
    action: str
    expected: str


@dataclass
class TestCase:
    id: str
    title: str
    requirement_id: Optional[str]
    priority: str
    steps: List[TestCaseStep] = field(default_factory=list)
