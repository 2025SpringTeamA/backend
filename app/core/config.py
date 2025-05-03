from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # OpenAI API key
    # openai_api_key: str
    # OpenAI Model
    # openai_model: str ="gpt-4.1-nano"

    # Database
    mysql_root_password: str
    mysql_database: str
    mysql_user: str
    mysql_password: str
    database_url: str
    admin_pin_code: int

    class Config:
        env_file = ".env"

settings = Settings()