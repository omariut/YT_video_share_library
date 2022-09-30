from videos.api.models import VideoIn, VideoOut, VideoUpdate
from  videos.api.db import videos, database
import os
import requests

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="videos/token",
    scheme_name="JWT"
)






GET_CURRENT_USER_URL = 'http://localhost:8000/users/users/remote/me/'



def get_current_user(token: str = Depends(reuseable_oauth)):
    token_type="Bearer"
    headers = {'content-type': 'application/json', 'Authorization':f'{token}'}
    r = requests.get(GET_CURRENT_USER_URL,headers=headers)
    return r.json()


async def verify_video_owner(id,user):
    query = videos.select(videos.c.id==id)
    video = await database.fetch_one(query=query)
    return video.username==user.get("username")


async def add_video(code,user):
    video = {"code":code,"username":user.get("username"),"total_likes":0,"total_dislikes":0,"total_comments":0 }
    query = videos.insert().values(**video)
    id =await database.execute(query=query)
    query = videos.select(videos.c.id==id)
    return await database.fetch_one(query=query)
    
async def increase_view(id,total_views):
    query = (
        videos
        .update()
        .where(videos.c.id == id)
        .values(total_views=total_views)
    )
    await database.execute(query=query)

async def get_all_videos():
    query = videos.select()
    return await database.fetch_all(query=query)

async def get_video(id):
    query = videos.select(videos.c.id==id)
    return await database.fetch_one(query=query)

async def delete_video(id: int,user=Depends(get_current_user)):
    video = await get_video(id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    is_owner=await verify_video_owner(id,user)
    if is_owner:
        query = videos.delete().where(videos.c.id==id)
        return await database.execute(query=query)
    else:
        raise HTTPException(status_code=404, detail="User is not video owner")


# async def update_video(id: int, payload: VideoIn):
#     query = (
#         videos
#         .update()
#         .where(videos.c.id == id)
#         .values(**payload.dict())
#     )
#     return await database.execute(query=query)