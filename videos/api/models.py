from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Union


class VideoIn(BaseModel):
    url: HttpUrl


class UserOut(BaseModel):
    id: str
    email: str
    username: str


class VideoOut(BaseModel):
    id: int
    code: str
    username: str
    total_likes: Optional[int] = None
    total_dislikes: Optional[int] = None
    total_comments: Optional[int] = None
    total_views: Optional[int] = None


class CommentOut(BaseModel):
    text: str
    username: str


class DetailsVideoOut(VideoOut):
    likes: List[str]
    dislikes: List[str]
    comments: List[CommentOut]


class VideoUpdate(VideoIn):
    url: HttpUrl


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
