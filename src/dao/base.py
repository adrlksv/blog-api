from sqlalchemy import select, insert, update

from src.database import async_session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)

            return result.scalar_one_or_none()
        
    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)

            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model)

            result = await session.execute(stmt)
            await session.commit()

            return result

    @classmethod
    async def update(cls, model_id: int, user_id: int, **data):
        async with async_session_maker() as session:
            stmt = (
                update(cls.model)
                .where(cls.model.id == model_id, cls.model.author_id == user_id)
                .values(**data).returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()

            return result.scalar_one_or_none()
