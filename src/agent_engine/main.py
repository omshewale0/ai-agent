from fastapi import FastAPI, Header, HTTPException

from .channels.whatsapp import WhatsAppInbound
from .config import settings
from .workflow import run_automation

app = FastAPI(title="AI Agent Engine")


@app.get("/health")
def health() -> dict:
    return {"ok": True, "provider": settings.llm_provider}


@app.post("/webhook/whatsapp")
async def whatsapp_webhook(
    payload: dict,
    x_verify_token: str | None = Header(default=None),
) -> dict:
    # Simple guard token. Replace with provider-specific signature verification in production.
    if x_verify_token and x_verify_token != settings.whatsapp_verify_token:
        raise HTTPException(status_code=401, detail="Invalid verification token")

    inbound = WhatsAppInbound.from_payload(payload)
    reply = await run_automation(inbound.text)

    # In production, send `reply` back via WhatsApp API here.
    return {"to": inbound.from_, "reply": reply}
