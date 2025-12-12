from __future__ import annotations

from typing import List

from app.models.requirements import Requirement


class ReqParserAgent:
    """Агент разбора требований.

    Сейчас используется очень простой хелпер:
    - для scenario_type="ui" каждая непустая строка превращается в Requirement
    - для scenario_type="api" поведение аналогичное, но с другим area
    """

    async def parse_requirements(
        self,
        *,
        scenario_type: str,
        source_type: str,
        content: str,
    ) -> List[Requirement]:
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        area = "ui" if scenario_type == "ui" else "api"

        requirements: List[Requirement] = []
        for idx, line in enumerate(lines, start=1):
            req = Requirement(
                id=f"{area}-{idx}",
                title=line[:80],
                description=line,
                area=area,
                priority="medium",
            )
            requirements.append(req)

        # На шаге реальной интеграции здесь можно звать LLM
        return requirements
