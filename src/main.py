from fastapi import FastAPI

from src.users.router import router as user_router
from src.posts.router import router as post_router


app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
