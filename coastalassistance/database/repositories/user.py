from sqlalchemy import select, update
from database.database import async_session
from database.models import User


async def add_user(user_id):
    async with async_session() as session:
        async with session.begin():
            query = select(User).filter(User.user_id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()

            if not user:
                new_user = User(user_id=user_id, username="", usertype=0, active=True)
                session.add(new_user)
                await session.commit()


async def update_username(username: str, user_id: int):
    async with async_session() as session:
        query = update(User).where(User.user_id == user_id).values(username=username)
        await session.execute(query)
        await session.commit()


async def check_exist_user(user_id: int) -> bool:
    async with async_session() as session:
        query = select(User).filter(User.user_id == user_id)
        result = await session.execute(query)
        is_exist = result.fetchone()
        if is_exist is None:
            return False
        else:
            return True


async def read_usertype(user_id: int) -> str:
    async with async_session() as session:
        query = select(User.usertype).filter(User.user_id == user_id)
        result = await session.execute(query)
        usertype = result.scalar()
        if usertype is None:
            return None
        elif usertype == 0:
            return "Пользователь"
        else:
            return "Администратор"
