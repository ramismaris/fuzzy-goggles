from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.database.dals import InformationChannelDAL
from web.database.models import User
from web.database.session import get_db
from web.schemas.information_channel import InformationChannelOut
from web.utils.authentication import get_current_user

router = APIRouter(prefix='/information_channel', tags=['Channel'])


@router.get('/', response_model=list[InformationChannelOut])
async def get_channels(session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await InformationChannelDAL.read(session)
