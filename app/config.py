from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings for App.

    In practice, these would be stored in a secure way via Secrets Manager,
    or in a .env during local development which would be ignored by git.
    """

    DATABASE_PORT: int = 5432
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    SQS_QUEUE: str = "http://localhost:4566/#000000000000/login-queue"
    APP_VERSION: int = 1
    FERNET_KEY: str = b"lIiSQJVcwPVDpJTxrthtKsfbEM4C1dvsS9BdD8GP3a4="


settings = Settings()
