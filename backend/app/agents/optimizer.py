from __future__ import annotations

from typing import Iterable, List, Set

from app.models.test_cases import TestCase


class OptimizationAgent:
    """Анализирует набор тестов, ищет дубли и пробелы."""

    async def analyze(self, test_cases: Iterable[TestCase]) -> List[str]:
        titles: Set[str] = set()
        duplicates: List[str] = []

        for tc in test_cases:
            title = tc.title.strip().lower()
            if title in titles:
                duplicates.append(tc.id)
            else:
                titles.add(title)

        messages: List[str] = []
        if duplicates:
            messages.append(f"Найдены дублирующиеся тесты: {', '.join(duplicates)}")
        else:
            messages.append("Дубликаты тест-кейсов не обнаружены.")

        # Более сложный анализ можно добавить позже
        return messages
