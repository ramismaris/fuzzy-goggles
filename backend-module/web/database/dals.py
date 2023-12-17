from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from web.database.models import User, Client, InformationChannel, Chat, Product


class UserDAL:
    @staticmethod
    async def create(db_session: AsyncSession, username: str, password: str) -> User:
        new_user = User(username=username, password=password)
        db_session.add(new_user)
        await db_session.commit()

        return new_user

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[User]:
        stmt = select(User).filter_by(**kwargs)
        users = await db_session.scalars(stmt)

        return users.fetchall()

    @staticmethod
    async def get(db_session: AsyncSession, username: str) -> User:
        stmt = select(User).filter_by(username=username)
        user = await db_session.scalar(stmt)

        return user


class ChatDAL:
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs) -> Chat:
        new_message = Chat(**kwargs)
        db_session.add(new_message)
        await db_session.commit()

        return new_message

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[Chat]:
        stmt = select(Chat).filter_by(**kwargs)
        chat = await db_session.scalars(stmt)

        return chat.fetchall()

    @staticmethod
    async def update(db_session: AsyncSession, question_id: int, **kwargs) -> Chat:
        result = await db_session.execute(
            update(Chat).where(Chat.id == question_id).values(kwargs).returning(Chat)
        )
        await db_session.commit()
        return result.scalar_one_or_none()


class InformationChannelDAL:
    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[InformationChannel]:
        stmt = select(InformationChannel).filter_by(**kwargs)
        channels = await db_session.scalars(stmt)

        return channels.fetchall()


class ClientDAL:
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs) -> Client:
        new_client = Client(**kwargs)
        db_session.add(new_client)
        await db_session.commit()

        return new_client

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[Client]:
        stmt = select(Client).filter_by(**kwargs)
        clients = await db_session.scalars(stmt)

        return clients.fetchall()

    @staticmethod
    async def delete(db_session: AsyncSession, **kwargs) -> None:
        stmt = delete(Client).filter_by(**kwargs)
        await db_session.execute(stmt)
        await db_session.commit()


class ProductDAL:
    @staticmethod
    async def create(db_session: AsyncSession, **kwargs) -> Product:
        new_product = Product(**kwargs)
        db_session.add(new_product)
        await db_session.commit()

        return new_product

    @staticmethod
    async def read(db_session: AsyncSession, **kwargs) -> list[Product]:
        stmt = select(Product).filter_by(**kwargs)
        products = await db_session.scalars(stmt)

        return products.fetchall()
