import httpx


async def get_user(id):
    r = httpx.get(f"http://localhost:8000/users/users/{id}")
    return r.json()


async def get_likes(video_id):
    r = httpx.get(f"http://127.0.0.1:8003/likes/likes-by-videos?video_id={video_id}")
    likes = r.json()
    return [item["username"] for item in likes]


async def get_dislikes(video_id):
    r = httpx.get(
        f"http://127.0.0.1:8003/dislikes/dislikes-by-video?video_id={video_id}"
    )
    dislikes = r.json()
    return [item["username"] for item in dislikes]


async def get_comments(video_id):
    r = httpx.get(
        f"http://127.0.0.1:8003/comments/comments-by-videos?video_id={video_id}"
    )
    comments = r.json()
    [[item.pop("video_id"), item.pop("id")] for item in comments]
    return comments
