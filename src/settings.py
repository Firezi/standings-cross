from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_DSN: str = "postgres://test:test@localhost:5432/standings_cross"
    JWT_SECRET_KEY: str = "70ce6838b5f99e5b4dac16c0f5ba0ba3b494c0328bae24e74dc77fc882ddac5e"


settings = Settings()
