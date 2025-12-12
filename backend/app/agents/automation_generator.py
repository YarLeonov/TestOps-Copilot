from __future__ import annotations

from typing import Iterable, List

from app.models.test_cases import TestCase
from app.models.testsuite import CodeBundle


PYTEST_HEADER = """import pytest


"""


class AutomationGeneratorAgent:
    """Агент генерации кода автотестов (pytest).

    Для демо генерирует очень простой код с AAA структурой в комментариях.
    """

    async def generate_pytest_from_testcases(
        self,
        test_cases: Iterable[TestCase],
        *,
        target: str = "ui",
    ) -> List[CodeBundle]:
        lines: List[str] = [PYTEST_HEADER]

        for tc in test_cases:
            func_name = self._to_function_name(tc.id, tc.title)
            lines.append(f"def {func_name}():")
            lines.append('    """')
            lines.append(f"    {tc.title}")
            lines.append("    """)

            lines.append("    # Arrange")
            lines.append("    # TODO: подготовка данных и окружения")

            lines.append("    # Act")
            lines.append("    # TODO: выполнение целевого действия")

            lines.append("    # Assert")
            lines.append("    # TODO: проверки результатов")
            lines.append("")

        content = "\n".join(lines)

        bundle = CodeBundle(
            name=f"test_{target}_generated.py",
            language="python",
            content=content,
        )
        return [bundle]

    def _to_function_name(self, test_id: str, title: str) -> str:
        cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in title)
        while "__" in cleaned:
            cleaned = cleaned.replace("__", "_")
        cleaned = cleaned.strip("_")
        return f"test_{test_id.lower()}_{cleaned[:40]}"
