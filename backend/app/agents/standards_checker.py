from __future__ import annotations

from typing import List

from app.schemas.generation import GenerationResponse


class StandardsCheckerAgent:
    """Проверка соответствия тестов базовым правилам (AAA и теги)."""

    async def validate_code(self, code: str) -> GenerationResponse:
        warnings: List[str] = []

        if "Arrange" not in code:
            warnings.append("Не найдена секция Arrange")
        if "Act" not in code:
            warnings.append("Не найдена секция Act")
        if "Assert" not in code:
            warnings.append("Не найдена секция Assert")
        if "pytest" not in code:
            warnings.append("Модуль не импортирует pytest")

        summary = "Проверка завершена. Нарушения не найдены." if not warnings else "Проверка завершена. Найдены замечания."

        return GenerationResponse(
            project_id=None,
            summary=summary,
            manual_test_cases=[],
            code_bundles=[],
            warnings=warnings,
        )
