from tortoise import Tortoise

from src.settings import settings


TORTOISE_ORM: dict = {
    "connections": {"default": settings.DB_DSN},
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
