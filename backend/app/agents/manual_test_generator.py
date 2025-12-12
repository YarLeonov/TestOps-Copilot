from __future__ import annotations

from typing import List

from app.models.requirements import Requirement
from app.models.test_cases import TestCase, TestCaseStep


class ManualTestGeneratorAgent:
    """Генерирует ручные тест-кейсы на основе требований."""

    async def generate_from_requirements(
        self,
        requirements: List[Requirement],
        *,
        max_tests: int = 20,
    ) -> List[TestCase]:
        test_cases: List[TestCase] = []

        for idx, req in enumerate(requirements[:max_tests], start=1):
            steps = [
                TestCaseStep(order=1, action="Открыть тестируемое приложение", expected="Приложение доступно"),
                TestCaseStep(order=2, action=f"Реализовать сценарий: {req.title}", expected="Сценарий выполняется без ошибок"),
            ]

            tc = TestCase(
                id=f"TC-{idx:03d}",
                title=f"{req.area.upper()} - {req.title}",
                requirement_id=req.id,
                priority=req.priority,
                steps=steps,
            )
            test_cases.append(tc)

        return test_cases
