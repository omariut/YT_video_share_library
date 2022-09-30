from reactions.api.models import CommentIn,CommentOut
from  reactions.api.db import comments, database
import os
import requests
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from reactions.api.user import get_current_user
from reactions.api.videos import get_video,increase_count

async def get_comment_by_video_and_user(video_id,username):
    query = comments.select().where(comments.c.video_id==video_id,comments.c.username==username)
    return await database.fetch_all(query=query)

async def get_all_comments_by_video(video_id):
    query = comments.select().where(comments.c.video_id==video_id)
    return await database.fetch_all(query=query)

async def get_comment(id):
    query=comments.select().where(comments.c.id==id)
    return await database.fetch_one(query=query)

async def add_comment(comment,username):
    comment=comment.dict()
    video_id=comment.get('video_id')
    video = await get_video(video_id)
    if not video:
        raise HTTPException("Video not found")
    
    comment["username"]=username
    query = comments.insert().values(**comment)
    id= await database.execute(query=query)
    all_comments=await get_all_comments_by_video(video_id)
    total_comments=len(all_comments)
    await increase_count(video_id, "comment", total_comments)
    return await get_comment(id)

async def update_comment(id: int, text:str):
    query = (
        comments
        .update()
        .where(comments.c.id == id)
        .values(text=text)
    )
    await database.execute(query=query)
    return await get_comment(id)

async def delete_comment(video_id,username):
    video = await get_video(video_id)
    if not video:
        raise HTTPException("Video not found")
    query = comments.delete().where(comments.c.video_id==video_id,comments.c.username==username)
    return await database.execute(query=query)



    
    
  