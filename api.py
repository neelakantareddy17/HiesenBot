from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from src.agent import build_agent

app = FastAPI()

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://orbiiit.vercel.app",
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

STYLE_RULES = (
    "Reply in a short, friendly, and humorous tone. "
    "Keep answers brief — usually around 40 to 60 words. "
    "Avoid long explanations. Be playful when appropriate, "
    "but never rude or offensive."
)

def soften_trim(text: str, max_words=70):
    words = text.split()
    return " ".join(words[:max_words]) if len(words) > max_words else text

@app.post("/askme")
async def ask_me(q: Query):
    prompt = f"{STYLE_RULES}\nUser: {q.message}\nAssistant:"
    reply = agent(prompt)
    reply = soften_trim(reply)
    return {"reply": reply}

@app.get("/")
async def root():
    return {"status": "ok"}

# Dynamic CORS-safe preflight handler (works for localhost + Vercel)
@app.options("/askme")
async def ask_me_options(request: Request):
    origin = request.headers.get("origin")

    if origin not in ALLOWED_ORIGINS:
        origin = "https://orbiiit.vercel.app"  # safe fallback

    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )
