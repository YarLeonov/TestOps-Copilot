import pytest

from app.core.llm_client import llm_client


@pytest.mark.asyncio
async def test_llm_client_stub_returns_text():
    text = await llm_client.generate("simple prompt")
    assert isinstance(text, str)
    assert text != ""
