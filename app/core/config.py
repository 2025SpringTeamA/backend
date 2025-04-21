from pydantic import BaseSettings

class Settings(BaseSettings):
    # OpenAI API key
    openai_api_key: str
    # OpenAI Model
    openai_model: str ="gpt-4.1-nano"

    # Database
    mysql_root_password: str
    mysql_database: str
    mysql_user: str
    mysql_password: str
    database_url: str

    class Config:
        env_file = ".env"