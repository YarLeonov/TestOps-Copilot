from __future__ import annotations

from typing import List

from app.agents.automation_generator import AutomationGeneratorAgent
from app.agents.manual_test_generator import ManualTestGeneratorAgent
from app.agents.standards_checker import StandardsCheckerAgent
from app.models.test_cases import TestCase
from app.schemas.generation import (
    AutomationGenerationRequest,
    CodeBundle,
    GenerationResponse,
    ManualGenerationRequest,
    ValidationRequest,
)
from app.services.requirements_service import RequirementsService


class TestCasesService:
    """Фасад для операций генерации и проверки тестов."""

    def __init__(
        self,
        requirements_service: RequirementsService | None = None,
        manual_agent: ManualTestGeneratorAgent | None = None,
        automation_agent: AutomationGeneratorAgent | None = None,
        standards_agent: StandardsCheckerAgent | None = None,
    ) -> None:
        self.requirements_service = requirements_service or RequirementsService()
        self.manual_agent = manual_agent or ManualTestGeneratorAgent()
        self.automation_agent = automation_agent or AutomationGeneratorAgent()
        self.standards_agent = standards_agent or StandardsCheckerAgent()

    async def generate_manual(self, request: ManualGenerationRequest) -> GenerationResponse:
        requirements = await self.requirements_service.parse(request)
        test_cases: List[TestCase] = await self.manual_agent.generate_from_requirements(
            requirements,
            max_tests=request.max_tests,
        )

        manual_descriptions = [
            f"{tc.id}: {tc.title}" for tc in test_cases
        ]

        return GenerationResponse(
            project_id=request.project_id,
            summary=f"Сгенерировано {len(test_cases)} ручных тест-кейсов",
            manual_test_cases=manual_descriptions,
            code_bundles=[],
            warnings=[],
        )

    async def generate_automation(self, request: AutomationGenerationRequest) -> GenerationResponse:
        # На хакатоне можно использовать сырые manual_test_cases для генерации
        synthetic_testcases: List[TestCase] = []
        for idx, text in enumerate(request.manual_test_cases, start=1):
            tc = TestCase(
                id=f"TC-AUTO-{idx:03d}",
                title=text[:80],
                requirement_id=None,
                priority="medium",
                steps=[],
            )
            synthetic_testcases.append(tc)

        code_bundles = await self.automation_agent.generate_pytest_from_testcases(
            synthetic_testcases,
            target=request.target,
        )

        return GenerationResponse(
            project_id=request.project_id,
            summary=f"Сгенерировано {len(code_bundles)} файлов с автотестами",
            manual_test_cases=[],
            code_bundles=[
                CodeBundle(name=bundle.name, language=bundle.language, content=bundle.content)
                for bundle in code_bundles
            ],
            warnings=[],
        )

    async def validate_tests(self, request: ValidationRequest) -> GenerationResponse:
        result = await self.standards_agent.validate_code(request.code)
        # Прокидываем project_id в ответ
        result.project_id = request.project_id
        return result
