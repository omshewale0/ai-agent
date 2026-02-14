import pytest

from src.agent_engine.workflow import run_automation


@pytest.mark.asyncio
async def test_pricing_rule():
    reply = await run_automation("Can I get pricing?")
    assert "₹999" in reply


@pytest.mark.asyncio
async def test_demo_rule():
    reply = await run_automation("Need a demo")
    assert "demo" in reply.lower()
