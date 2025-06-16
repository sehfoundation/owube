import os
from fastapi import Depends
from fastapi_users import FastAPIUsers, schemas
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from .db import database, User


SECRET = os.getenv("SECRET_KEY", "SUPERSECRET_KEY")
jwt_authentication = JWTAuthentication(
    secret=SECRET,
    lifetime_seconds=3600,
    token_url="auth/jwt/login"
)


class UserCreate(schemas.BaseUserCreate):
    pass

class UserRead(schemas.BaseUser[int]):
    pass

class UserUpdate(schemas.BaseUserUpdate):
    pass


DATABASE_URL = database.url
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


fastapi_users = FastAPIUsers[
    User,
    int
](
    get_user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserRead
)


get_auth_router = fastapi_users.get_auth_router(jwt_authentication)
get_register_router = fastapi_users.get_register_router()
get_users_router = fastapi_users.get_users_router()
