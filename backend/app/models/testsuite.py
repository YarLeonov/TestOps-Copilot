from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from app.schemas.generation import CodeBundle
from app.models.test_cases import TestCase


@dataclass
class TestSuite:
    """Набор тестов и связанный с ними код."""

    project_id: str
    test_cases: List[TestCase] = field(default_factory=list)
    code_bundles: List[CodeBundle] = field(default_factory=list)


@dataclass
class CodeBundle(TestSuite.__annotations__["code_bundles"].__args__[0]):  # type: ignore
    """Алиас на CodeBundle из схем, чтобы не дублировать."""
    pass
