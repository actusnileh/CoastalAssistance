from requests import delete
from sqlalchemy import select, update
from database.models import Shore
from database.database import async_session


async def add_shores(user_id, photo, geo_tag, about, destruction, activated):
    async with async_session() as session:
        shore = Shore(
            user_id=user_id,
            photo=photo,
            geo_tag=geo_tag,
            about=about,
            destruction=destruction,
            activated=activated,
        )
        session.add(shore)
        await session.commit()


async def user_shores(user_id):
    async with async_session() as session:
        query = select(Shore).filter(Shore.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()


async def coordinates_shores():
    async with async_session() as session:
        query = select(
            Shore.geo_tag, Shore.about, Shore.photo, Shore.destruction, Shore.activated
        )
        result = await session.execute(query)
        return result.all()


async def read_count_photos(user_id):
    async with async_session() as session:
        query = select(Shore).filter(Shore.user_id == user_id)
        result = await session.execute(query)
        return len(result.all())


async def info_if_activated_zero():
    async with async_session() as session:
        query = select(Shore).filter(Shore.activated == 0)
        result = await session.execute(query)
        return result.all()


async def activated_to_one(id):
    async with async_session() as session:
        query = update(Shore).where(Shore.id == id).values(activated=1)
        await session.execute(query)
        await session.commit()


async def update_destruction(id, new_destruction_value):
    async with async_session() as session:
        query = (
            update(Shore)
            .where(Shore.id == id)
            .values(destruction=new_destruction_value)
        )
        await session.execute(query)
        await session.commit()


async def update_about(id, new_about_value):
    async with async_session() as session:
        query = update(Shore).where(Shore.id == id).values(about=new_about_value)
        await session.execute(query)
        await session.commit()


async def delete_by_id(id):
    async with async_session() as session:
        query = delete(Shore).where(Shore.id == id)
        await session.execute(query)
        await session.commit()
