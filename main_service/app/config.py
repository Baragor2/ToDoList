from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    ALGORITHM: str
    TG_HASH_ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    class Config:
        env_file = ".env-non-dev"


settings = Settings()


BASE_DIR = Path(__file__).parent.parent


class AuthSettings(BaseSettings):
    private_key_pass: Path = BASE_DIR / "secret_key.pem"


auth_settings = AuthSettings()


class CommentsSettings(BaseSettings):
    COMMENTS_API_ROOT: str = "http://localhost:8001/"


comments_settings = CommentsSettings()
