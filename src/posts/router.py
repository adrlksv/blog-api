from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache

from src.auth.dependencies import get_current_user
from src.posts.schemas import SPost
from src.users.models import User
from src.posts.dao import PostsDAO
from src.exceptions import PostDeleteError

from datetime import datetime

import logging


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("")
async def get_all_posts(
    current_user: User = Depends(get_current_user)
):
    return await PostsDAO.get_posts_by_user_id(current_user.id)


@router.get("/{post_id}")
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user)
):
    return await PostsDAO.get_post_by_id(post_id=post_id)


@router.post("")
async def create_post(
    data: SPost,
    current_user: User = Depends(get_current_user)
):
    await PostsDAO.add(
        title=data.title,
        content=data.content,
        is_published=True,
        author_id=current_user.id,
    )

    redis = FastAPICache.get_backend().redis
    today = datetime.utcnow().strftime("%Y-%m-%d")
    key = f"user:{current_user.id}:posts:{today}"
    await redis.incr(key)

    now = datetime.utcnow()
    end_of_day = datetime.utcnow().replace(hour=23, minute=59, second=59, microsecond=999999)
    ttl_seconds = (end_of_day - now).total_seconds()

    await redis.expire(key, int(ttl_seconds))

    return {
        "message": "Post added successfully"
    }


@router.put("/{post_id}")
async def update_post(
    post_id: int,
    data: SPost,
    current_user: User = Depends(get_current_user)
):
    updated_post = await PostsDAO.update(
        model_id=post_id,
        user_id=current_user.id,
        title=data.title,
        content=data.content,
        is_published=True,
    )

    return updated_post


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user)
):
    post = await PostsDAO.delete_post(post_id)

    if not post:
        raise PostDeleteError

    return {
        "message": "post deleted successfully"
    }


@router.get("/stats/posts")
async def get_post_stats(current_user: User = Depends(get_current_user)):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    key = f"user:{current_user.id}:posts:{today}"
    redis = FastAPICache.get_backend().redis
    count = await redis.get(key)

    if count:
        count = int(count.decode("utf-8"))
    else:
        count = 0

    logger.debug(f"Key: {key}, Count: {count}")
    
    return {
        "created_posts_today": count
    }
