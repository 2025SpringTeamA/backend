from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # PIN code
    ADMIN_PIN_CODE: str

    # OpenAI API key
    openai_api_key: str
    # OpenAI Model
    openai_model: str ="gpt-4.1-nano"
    
    
    # AWS Bedrock
    MODEL_ID : str ="anthropic.claude-instant-v1"
    REGION : str ="ap-northeast-1"
    
    
    
    # AWS S3
    # aws_access_key_id: str
    # aws_secret_access_key: str
    # aws_s3_bucket_name: str
    # aws_region: str = "ap-northeast-1"


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