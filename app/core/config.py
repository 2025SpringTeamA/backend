import os
from pydantic_settings import BaseSettings

# ローカル環境のみ .env を読み込む
if os.getenv("ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # PIN code
    ADMIN_PIN_CODE: str

    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4.1-nano"

    # AWS Bedrock
    MODEL_ID: str = "anthropic.claude-instant-v1"
    REGION: str = "ap-northeast-1"

    # Database
    mysql_root_password: str
    mysql_database: str
    mysql_user: str
    mysql_password: str
    database_url: str
    admin_pin_code: int

    class Config:
        env_file = ".env"  # ローカルで .env を参照するように設定

settings = Settings()
