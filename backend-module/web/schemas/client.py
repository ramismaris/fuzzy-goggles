from datetime import datetime

from pydantic import BaseModel


class ClientIn(BaseModel):
    username: str
    gender: str
    age: float


class ClientOut(BaseModel):
    id: int
    username: str
    gender: str
    age: float
    created_at: datetime
