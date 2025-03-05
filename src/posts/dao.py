from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao.base import BaseDAO
from src.posts.models import Post


class PostsDAO(BaseDAO):
    model = Post

    @classmethod
    async def get_posts_by_user_id(cls, session: AsyncSession, user_id):
        query = (
            select(Post)
            .filter_by(author_id=user_id)
        )
        result = await session.execute(query)

        return result.scalars().all()
    
    @classmethod
    async def get_post_by_id(cls, session: AsyncSession, post_id: int):
        query = (
            select(Post)
            .filter_by(
                id=post_id
            )
        )
        result = await session.execute(query)
            
        return result.scalar_one_or_none()
        
    @classmethod
    async def delete_post(cls, session: AsyncSession, post_id: int):
        stmt = (
            delete(Post)
            .where(Post.id == post_id)
        )
        await session.execute(stmt)
        await session.commit()
