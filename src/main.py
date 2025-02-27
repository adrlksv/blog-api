from fastapi import FastAPI
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

from redis import asyncio as aioredis

from src.users.router import router as user_router
from src.posts.router import router as post_router

from contextlib import asynccontextmanager

from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    await redis.close()


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(post_router)
