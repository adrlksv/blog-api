from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_user
from src.posts.schemas import SPost
from src.users.models import User
from src.posts.dao import PostsDAO


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
    await PostsDAO.delete_post(post_id)

    return {
        "message": "post deleted successfully"
    }
