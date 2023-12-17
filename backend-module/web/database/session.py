import asyncio
import json
import os
from typing import AsyncGenerator

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from web.config import DATABASE_URL
from web.database.dals import ProductDAL
from web.database.models import Base

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await create_channels(conn)
    await create_products()


async def create_channels(conn):
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/utils/backup.sql'
    with open(path) as file:
        queries = file.readlines()
        for query in queries:
            await conn.execute(text(query))


async def create_products():
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/utils/products.json'
    with open(path) as file:
        data = json.load(file)

    async with async_session() as session:
        for product_str in data:
            await ProductDAL.create(session, **product_str)

        # products = await ProductDAL.read(session)
        # for product in products:
        #     product_dict = {key: value for key, value in product.__dict__.items() if not key.startswith('_')}
        #     print(json.dumps(ProductOutForModel(**product_dict).model_dump(), indent=4, ensure_ascii=False))


if __name__ == '__main__':
    asyncio.run(main())
