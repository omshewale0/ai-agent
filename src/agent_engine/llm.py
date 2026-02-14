from __future__ import annotations

import httpx
from .config import settings


class LLMError(RuntimeError):
    pass


async def generate_reply(user_text: str) -> str:
    provider = settings.llm_provider.lower().strip()
    if provider == "openai":
        return await _openai_reply(user_text)
    if provider == "ollama":
        return await _ollama_reply(user_text)
    raise LLMError(f"Unsupported provider: {provider}")


async def _openai_reply(user_text: str) -> str:
    if not settings.openai_api_key:
        return "OPENAI_API_KEY missing. Please configure it in .env"

    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for customer support."},
            {"role": "user", "content": user_text},
        ],
    }
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()


async def _ollama_reply(user_text: str) -> str:
    url = f"{settings.ollama_base_url.rstrip('/')}/api/generate"
    payload = {
        "model": settings.ollama_model,
        "prompt": f"You are a helpful assistant for customer support. User: {user_text}",
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")
