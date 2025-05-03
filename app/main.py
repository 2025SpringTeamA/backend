from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os
from api.endpoints.auth import router as auth_router
from api.endpoints.user import router as user_router
from api.endpoints.session import router as session_router
from api.endpoints.message import router as message_router
from api.endpoints.generated_media import router as generated_media_router


app = FastAPI()


# ✅ CORS設定（Next.jsからアクセス可能にする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要なら "http://localhost:3000" などに限定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI + MySQL in Docker!"}

@app.get("/db-status")
def db_status():
    try:
        connection = mysql.connector.connect(
            host="db",  # ← Dockerコンテナ名
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        if connection.is_connected():
            connection.close()  # ✅ 接続が確認できたら明示的にクローズ
            return {"db_status": "connected"}
        else:
            return {"db_status": "not connected"}
    except Exception as e:
        return {"db_status": "error", "details": str(e)}


# 認証用エンドポイント
app.include_router(auth_router, prefix="/api", tags=["auth"])

# アカウント情報用エンドポイント
app.include_router(user_router, prefix="/api", tags=["user"])

# チャット用エンドポイント
app.include_router(session_router, prefix="/api", tags=["session"])

# メッセージ用エンドポイント
app.include_router(message_router, prefix="/api", tags=["message"])

# 生成用エンドポイント
app.include_router(generated_media_router, prefix="/api", tags=["generated_media"])