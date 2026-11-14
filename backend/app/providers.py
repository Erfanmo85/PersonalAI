import asyncio
from openai import AsyncOpenAI
from . import config

_client = AsyncOpenAI(
    base_url=config.BASE_URL,
    api_key=config.API_KEY or "missing",
    default_headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36",
        "Accept": "application/json",
    },
)

def _err(model, e):
    body = getattr(getattr(e, "response", None), "text", "")
    print(f"[{model}] error: {e} | {body[:300]}")

async def ask(model, messages):
    try:
        r = await asyncio.wait_for(
            _client.chat.completions.create(
                model=model, messages=messages, max_tokens=config.PROPOSER_MAX_TOKENS),
            config.TIMEOUT,
        )
        c = r.choices[0]
        if not c.message.content:
            print(f"[{model}] empty answer, finish_reason={c.finish_reason}")
            return None
        return c.message.content
    except Exception as e:
        _err(model, e)
        return None

async def stream(model, messages):
    try:
        s = await _client.chat.completions.create(
            model=model, messages=messages, stream=True, max_tokens=config.JUDGE_MAX_TOKENS)
        async for chunk in s:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        _err(model, e)
        yield "⚠️ خطا در ارتباط با مدل داور (جزئیات در ترمینال بک‌اند)"