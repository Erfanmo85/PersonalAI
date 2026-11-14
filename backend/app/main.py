from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from . import config, db
from .ensemble import answer_stream

app = FastAPI(title="Mostashar")
app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS,
                   allow_methods=["*"], allow_headers=["*"])

def auth(authorization: str = Header(default="")):
    if not config.APP_TOKEN or authorization != f"Bearer {config.APP_TOKEN}":
        raise HTTPException(401, "Unauthorized")

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat", dependencies=[Depends(auth)])
async def chat(req: ChatRequest):
    if not config.JUDGE or not config.API_KEY:
        raise HTTPException(500, "BEATAPI_API_KEY یا JUDGE در .env تنظیم نشده است")
    return StreamingResponse(answer_stream(req.message), media_type="text/plain; charset=utf-8")

@app.get("/api/history", dependencies=[Depends(auth)])
def history():
    return db.recent(100)

@app.delete("/api/history", dependencies=[Depends(auth)])
def clear_history():
    db.clear()
    return {"ok": True}

@app.get("/api/health")
def health():
    return {"bot": config.BOT_NAME, "proposers": config.PROPOSERS, "judge": config.JUDGE, "key_set": bool(config.API_KEY)}
