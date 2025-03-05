from fastapi import APIRouter, Depends
from fastapi_cache import FastAPICache

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.posts.schemas import SPost
from src.users.models import User
from src.posts.dao import PostsDAO
from src.database import get_db

from datetime import datetime

import logging


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.get("")
async def get_all_posts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await PostsDAO.get_posts_by_user_id(
        session=db,
        user_id=current_user.id
    )


@router.get("/{post_id}")
async def get_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await PostsDAO.get_post_by_id(
        session=db,
        post_id=post_id
    )


@router.post("")
async def create_post(
    data: SPost,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await PostsDAO.add(
        session=db,
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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    updated_post = await PostsDAO.update(
        session=db,
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
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await PostsDAO.delete_post(
        session=db,
        post_id=post_id
    )

    return {
        "message": "post deleted successfully"
    }


@router.get("/stats/posts")
async def get_post_stats(
    current_user: User = Depends(get_current_user)
):
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
