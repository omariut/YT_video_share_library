from users.api.models import TokenSchema,TokenPayload,UserAuth,UserOut,SystemUser
from  users.api.db import users, database

from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils import (
    ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError


async def add_user(user):
    query = users.insert().values(**user)
    id =await database.execute(query=query)
    query = users.select(users.c.id==id)
    return await database.fetch_one(query=query)
    
    
  

async def get_all_users():
    query = users.select()
    return await database.fetch_all(query=query)

async def get_user(email):
    query = users.select(users.c.email==email)
    return await database.fetch_one(query=query)
async def get_user_by_id(id):
    query = users.select(users.c.id==id)
    return await database.fetch_one(query=query)
async def delete_user(id: int):
    query = users.delete().where(users.c.id==id)
    return await database.execute(query=query)

# async def update_user(id: int, payload: VideoIn):
#     query = (
#         users
#         .update()
#         .where(users.c.id == id)
#         .values(**payload.dict())
#     )
#     return await database.execute(query=query)


reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/users/users/login",
    scheme_name="JWT"
)



async def get_user_from_token(token):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )

        token_data = TokenPayload(**payload)

        
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user: Union[dict[str, Any], None] = await get_user(token_data.sub)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    
    return SystemUser(**user)


async def get_current_user(token: str = Depends(reuseable_oauth)) -> SystemUser:
    return await get_user_from_token(token)    

async def get_current_user_remote(token:str):
    return await get_user_from_token(token)  