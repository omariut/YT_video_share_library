from typing import List,Union,Dict
from fastapi import Header, APIRouter, HTTPException

from reactions.api.models import LikeIn,LikeOut,DislikeIn,DislikeOut
from reactions.api.db_manager import dislikes as db_dislikes

from fastapi import Depends
import requests
dislikes = APIRouter()
#verify_video_owner



@dislikes.get('/dislikes-by-video', response_model=List[DislikeOut],summary="All Dislikes by videos")
async def index(video_id:int):
    return await db_dislikes.get_all_dislikes_by_video(video_id)

@dislikes.post('/', response_model=Union[DislikeOut,None],summary="add remove dislikes", status_code=201)
async def add_remove_dislike(id:int,user=Depends(db_dislikes.get_current_user)):
    return await db_dislikes.add_remove_dislike(id, user)





