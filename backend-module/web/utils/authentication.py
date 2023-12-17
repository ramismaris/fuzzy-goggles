from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from web.config import SECRET_KEY
from web.database.dals import UserDAL
from web.database.session import get_db
from web.utils.hashing import Hasher

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60  # = сутки


class Auth(BaseModel):
    username: str
    password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/login')


async def authenticate_user(session, username: str, password: str):
    user = await UserDAL.get(session, username)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


class TokenData(BaseModel):
    username: str


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await UserDAL.get(session, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
