# AI Agent Engine (Automation + Multi-channel + WhatsApp Auto Reply)

हा starter project तुम्हाला असा AI agent engine बनवायला मदत करतो जो:

- Open-source LLM वापरू शकतो (उदा. **Ollama**)
- Paid API वापरू शकतो (उदा. **OpenAI**)
- Multi-channel integration करू शकतो
- WhatsApp message आल्यावर auto-reply करू शकतो

## Features

- Provider abstraction (`openai` / `ollama`)
- Rule-based + LLM-based automation flow
- WhatsApp webhook endpoint (`/webhook/whatsapp`)
- Environment variable based secure config

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn src.agent_engine.main:app --reload --port 8080
```

## `.env` Example

```env
# Select provider: openai | ollama
LLM_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4o-mini

# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# WhatsApp security token (meta/twilio style webhook guard)
WHATSAPP_VERIFY_TOKEN=change-me
```

## WhatsApp webhook test

```bash
curl -X POST http://localhost:8080/webhook/whatsapp \
  -H 'Content-Type: application/json' \
  -d '{"from":"+919999999999","text":"Hi, mala pricing pahije"}'
```

Response मध्ये `reply` field येईल.

## Architecture

1. `channels/whatsapp.py`: incoming payload normalize
2. `workflow.py`: automation rules + LLM fallback
3. `llm.py`: selected provider call
4. `main.py`: FastAPI routes

## Next steps for production

- WhatsApp provider (Meta Cloud API / Twilio) outbound integration add करा
- Redis queue + worker add करा
- Conversation memory (Postgres / Vector DB) add करा
- Rate limit + signature verification harden करा
- Channel connectors: Email, Telegram, Instagram, Web chat
