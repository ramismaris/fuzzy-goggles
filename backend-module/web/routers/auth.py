from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from web.database.dals import UserDAL
from web.database.session import get_db
from web.schemas.auth import UserIn, UserOut, LoginOut
from web.utils.authentication import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, \
    get_current_user
from web.utils.hashing import Hasher

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/', response_model=UserOut)
async def register_user(body: UserIn, session: AsyncSession = Depends(get_db)):
    try:
        return await UserDAL.create(session, username=body.username, password=Hasher.get_password_hash(body.password))
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/login', response_model=LoginOut)
async def login_user(body: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    user = await authenticate_user(session, body.username, body.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/', response_model=UserOut)
async def info_about_user(user=Depends(get_current_user)):
    return user
