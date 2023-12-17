from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'web_users'

    id = Column(Integer, primary_key=True)

    username = Column(String, unique=True)
    password = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f'{self.id} - {self.username}'


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)

    text = Column(String, nullable=True)

    product_id = Column(ForeignKey('products.id'), nullable=True)
    channel_id = Column(ForeignKey('channels.id'), nullable=True)
    client_id = Column(ForeignKey('clients.id'), nullable=True)

    is_liked = Column(Boolean, nullable=True)
    question_id = Column(ForeignKey('chats.id'), nullable=True)

    user_id = Column(ForeignKey('web_users.id'))

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class InformationChannel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    description = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)

    title = Column(String)
    description = Column(String)
    interest_rate = Column(String)
    category = Column(String)
    advantages = Column(JSONB)
    conditions = Column(String)
    benefits = Column(String)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)

    username = Column(String)
    gender = Column(String)
    age = Column(Float)

    user_id = Column(ForeignKey('web_users.id'))

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
