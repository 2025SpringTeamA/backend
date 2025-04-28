from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
import os


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




# テスト
from api.endpoints import message
app.include_router(message.router)