from pydantic import BaseModel


class WhatsAppInbound(BaseModel):
    from_: str
    text: str

    @classmethod
    def from_payload(cls, payload: dict) -> "WhatsAppInbound":
        # Generic payload support for demo usage
        sender = payload.get("from") or payload.get("wa_id") or "unknown"
        text = payload.get("text") or payload.get("message") or ""
        return cls(from_=sender, text=text)
