from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from web.database.dals import ChatDAL, InformationChannelDAL, ProductDAL, ClientDAL
from web.database.models import User
from web.database.session import get_db
from web.schemas.chat import QuestionIn, QuestionPatchIn, ChatOut
from web.schemas.client import ClientOut
from web.schemas.information_channel import InformationChannelOut
from web.schemas.product import ProductOut
from web.utils.authentication import get_current_user
from web.utils.chat_model import get_model_answer

router = APIRouter(prefix='/chat', tags=['Chat'])


@router.get("/", response_model=list[ChatOut])
async def get_user_dialog(session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ChatDAL.read(session, user_id=current_user.id)


@router.post("/")
async def request_offer(
        body: QuestionIn, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    question = await ChatDAL.create(session, **body.model_dump(), user_id=current_user.id)

    product = await ProductDAL.read(session, id=question.product_id)
    channel = await InformationChannelDAL.read(session, id=question.channel_id)
    client = await ClientDAL.read(session, id=question.client_id)

    if len(product) == 0 or len(channel) == 0 or len(client) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    request_body = {
        'product': ProductOut(**product[0].__dict__).model_dump(),
        'channel': InformationChannelOut(**channel[0].__dict__).model_dump(),
        'client': ClientOut(**client[0].__dict__).model_dump()
    }
    ai_answer = await get_model_answer(request_body)
    if not ai_answer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    answer = await ChatDAL.create(session, text=ai_answer['text'], question_id=question.id, user_id=current_user.id)

    return answer


@router.patch("/{answer_id}")
async def mark_answer(
        answer_id: int, body: QuestionPatchIn,
        session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    question = await ChatDAL.read(session, id=answer_id)

    if len(question) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    if question[0].user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    await ChatDAL.update(session, question_id=question[0].id, **body.model_dump())

    # какая-то логика для дообучения модели
