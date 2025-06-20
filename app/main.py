from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

import os
from api.api import router as api_router



app = FastAPI()

# レートリミットの設定
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ✅ CORS設定（Next.jsからアクセス可能にする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要なら "http://localhost:3000" などに限定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "saburo-fastapi"}

app.include_router(api_router, prefix="/api")
