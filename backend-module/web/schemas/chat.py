from datetime import datetime

from pydantic import BaseModel


class ChatOut(BaseModel):
    id: int
    text: str | None = None
    product_id: int | None = None
    channel_id: int | None = None
    client_id: int | None = None
    is_liked: bool | None = None
    question_id: int | None = None
    user_id: int
    created_at: datetime
    updated_at: datetime


class QuestionIn(BaseModel):
    product_id: int
    channel_id: int
    client_id: int


class QuestionPatchIn(BaseModel):
    is_liked: bool
