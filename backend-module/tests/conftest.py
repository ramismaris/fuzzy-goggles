import asyncio
import os
from collections import namedtuple
from datetime import timedelta
from typing import Generator, AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from starlette.testclient import TestClient

from web.__main__ import app
from web.config import DATABASE_URL_TEST
from web.database.dals import UserDAL
from web.database.models import Base
from web.database.session import get_db
from web.utils.authentication import create_access_token

metadata = Base.metadata

engine = create_async_engine(DATABASE_URL_TEST, future=True, echo=False, poolclass=NullPool)
async_session = async_sessionmaker(engine, expire_on_commit=False)

path_to_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/tests/backup.sql'


async def override_get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
        await conn.execute(
            text("INSERT INTO public.channels (id, name, description, created_at, updated_at) VALUES (1, 'TMO', 'Колл центр (телемеркетинг)', '2023-12-16 00:47:19.000000', '2023-12-16 00:47:19.000000');")
        )
        await conn.execute(
            text("INSERT INTO public.products (id, title, description, interest_rate, category, advantages, conditions, benefits, created_at, updated_at) VALUES (1, 'Страхование для путешественников', 'Надежная защита вашего отдыха»', null, 'INS_LIFE', null, '', null, '2023-12-17 17:10:06.615689', '2023-12-17 17:10:06.615697');")
        )
    yield
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session')
async def auth() -> (int, str):
    user_data = {'username': 'test_user', 'password': 'password'}
    async with async_session() as session:
        user = await UserDAL.read(session, username=user_data['username'])
        if len(user) == 0:
            user = await UserDAL.create(session, user_data['username'], user_data['password'])
        else:
            user = user[0]

    access_token = create_access_token(
        data={"sub": user_data['username']}, expires_delta=timedelta(minutes=30)
    )

    Auth = namedtuple('Auth', ['user_id', 'access_token'])

    return Auth(user_id=user.id, access_token=access_token)
