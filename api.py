from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.agent import build_agent

app = FastAPI()

# Allow both local dev and Render frontend if needed later
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = build_agent()

class Query(BaseModel):
    message: str

@app.post("/askme")
async def ask_me(q: Query):
    reply = agent(q.message)
    return {"reply": reply}

# Health check (optional but useful)
@app.get("/")
async def root():
    return {"status": "ok"}

# Explicit preflight handler WITH headers (Render + Cloudflare safe)
@app.options("/askme")
async def ask_me_options():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )
