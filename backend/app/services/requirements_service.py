from __future__ import annotations

from typing import List

from app.agents.req_parser import ReqParserAgent
from app.models.requirements import Requirement
from app.schemas.generation import ManualGenerationRequest


class RequirementsService:
    """Сервис для работы с требованиями."""

    def __init__(self, agent: ReqParserAgent | None = None) -> None:
        self.agent = agent or ReqParserAgent()

    async def parse(self, request: ManualGenerationRequest) -> List[Requirement]:
        return await self.agent.parse_requirements(
            scenario_type=request.scenario_type,
            source_type=request.source_type,
            content=request.content,
        )
