from sqlalchemy import select, delete

from src.dao.base import BaseDAO
from src.posts.models import Post
from src.database import async_session_maker


class PostsDAO(BaseDAO):
    model = Post

    @classmethod
    async def get_posts_by_user_id(cls, user_id):
        async with async_session_maker() as session:
            query = (
                select(Post)
                .filter_by(author_id=user_id)
            )
            result = await session.execute(query)

            return result.scalars().all()
    
    @classmethod
    async def get_post_by_id(cls, post_id: int):
        async with async_session_maker() as session:
            query = (
                select(Post)
                .filter_by(
                    id=post_id
                )
            )
            result = await session.execute(query)
            
            return result.scalar_one_or_none()
        
    @classmethod
    async def delete_post(cls, post_id: int):
        async with async_session_maker() as session:
            stmt = (
                delete(Post)
                .where(Post.id == post_id)
            )
            await session.execute(stmt)
            await session.commit()
