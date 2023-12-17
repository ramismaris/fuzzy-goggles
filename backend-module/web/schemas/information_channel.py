from datetime import datetime

from pydantic import BaseModel


class InformationChannelOut(BaseModel):
    id: int
    name: str
    description: str
