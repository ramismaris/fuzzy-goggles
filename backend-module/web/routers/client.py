from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from web.database.dals import ClientDAL
from web.database.models import User
from web.database.session import get_db
from web.schemas.client import ClientIn, ClientOut
from web.utils.authentication import get_current_user

router = APIRouter(prefix='/client', tags=['Client'])


@router.get('/', response_model=list[ClientOut])
async def get_clients(session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await ClientDAL.read(session, user_id=current_user.id)


@router.post('/', response_model=ClientOut)
async def create_client(
        body: ClientIn, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        return await ClientDAL.create(session, **body.model_dump(), user_id=current_user.id)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete('/{client_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
        client_id: int, session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
):
    await ClientDAL.delete(session, user_id=current_user.id, id=client_id)
