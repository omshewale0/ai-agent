from __future__ import annotations

from .llm import generate_reply


async def run_automation(user_text: str) -> str:
    t = user_text.lower().strip()

    # Quick deterministic automations
    if "pricing" in t or "price" in t:
        return "Our plans start at ₹999/month. Need monthly or annual details?"

    if "demo" in t:
        return "Great! Please share your preferred date/time and team size for the demo."

    # LLM fallback
    return await generate_reply(user_text)
