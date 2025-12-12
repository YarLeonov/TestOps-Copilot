import pytest

from app.agents.manual_test_generator import ManualTestGeneratorAgent
from app.agents.req_parser import ReqParserAgent
from app.models.requirements import Requirement


@pytest.mark.asyncio
async def test_req_parser_simple_lines():
    agent = ReqParserAgent()
    content = "Первое требование\n\nВторое требование"
    reqs = await agent.parse_requirements(
        scenario_type="ui",
        source_type="text",
        content=content,
    )
    assert len(reqs) == 2
    assert reqs[0].title.startswith("Первое")


@pytest.mark.asyncio
async def test_manual_test_generator_creates_tests():
    reqs = [
        Requirement(
            id="ui-1",
            title="Проверка калькулятора",
            description="Требование",
            area="ui",
            priority="high",
        )
    ]
    agent = ManualTestGeneratorAgent()
    tests = await agent.generate_from_requirements(reqs, max_tests=5)
    assert len(tests) == 1
    assert tests[0].title
    assert tests[0].steps
