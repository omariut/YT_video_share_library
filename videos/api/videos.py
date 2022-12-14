from typing import List, Union
from fastapi import Header, APIRouter, HTTPException
from videos.api.utils import get_video_code
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from videos.api.models import VideoIn, VideoOut, TokenSchema, DetailsVideoOut
from videos.api import db_manager
from videos.api.service import get_user, get_likes, get_dislikes, get_comments
from fastapi import Depends
import requests
from videos.api.db import videos as db_videos, database

videos = APIRouter()
# verify_video_owner


@videos.post(
    "/token",
    summary="Create access and refresh tokens for user",
    response_model=TokenSchema,
    include_in_schema=False,
)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    login_url = "http://localhost:8000/users/users/login"
    payload = {"username": form_data.username, "password": form_data.password}
    r = requests.post(login_url, data=payload)
    return r.json()


@videos.get("/", response_model=List[VideoOut], summary="Homepage(all videos)")
async def index():
    return await db_manager.get_all_videos()


@videos.get("/{id}", response_model=VideoOut, include_in_schema=False)
async def single_video_page(id: int):
    video = await db_manager.get_video(id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@videos.get(
    "/play/{id}",
    response_model=DetailsVideoOut,
    summary="Video play Page.View counts increases here.",
)
async def video_play_page(id: int):
    video = await db_manager.get_video(id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if video.total_view:
        total_views = video.total_views + 1
    else:
        total_views = 1

    await db_manager.increase_view(id, total_views)
    likes = await get_likes(id)
    dislikes = await get_dislikes(id)
    comments = await get_comments(id)
    print(likes, dislikes, comments)
    video_details = DetailsVideoOut(
        **video, likes=likes, comments=comments, dislikes=dislikes
    )
    return video_details.dict()


@videos.post("/", response_model=VideoOut, status_code=201)
async def add_video(payload: VideoIn, user=Depends(db_manager.get_current_user)):
    code = get_video_code(payload.dict().get("url"))
    return await db_manager.add_video(code, user)


@videos.delete("/{id}", summary="Only owner can delete")
async def delete_video(id, x=Depends(db_manager.delete_video)):
    return x


@videos.get("/change_count/{id}", include_in_schema=False)
async def increase_count(id: int, object_type, total_count: int):
    print(total_count)
    if object_type == "like":
        query = (
            db_videos.update()
            .where(db_videos.c.id == id)
            .values(total_likes=total_count)
        )
    elif object_type == "dislike":
        query = (
            db_videos.update()
            .where(db_videos.c.id == id)
            .values(total_dislikes=total_count)
        )
    elif object_type == "comment":
        query = (
            db_videos.update()
            .where(db_videos.c.id == id)
            .values(total_comments=total_count)
        )

    await database.execute(query=query)
