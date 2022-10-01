# YT_video_share_library
- A FastAPI microservice project to share Youtube Videos where user can upload(url),play, comment,like, dislike videos
- 'user', 'video' and 'reactions' are three different services
- Unauthenticated users can see list and play videos
- Only logged in users can add video and make comments or reactions 
- User uploads YT video by adding YT urls
- video code will be stored and used to fetch video and thumbnails
- In homepage all thumbnails are shown along with total like, dislike,comment count
- In "play video" page user will get access to play the video
- In "play video" page user can see the list of who like,dislike, comment the video
- With every change(add,delete) like,dislike,comment count will be changed (increased or decreased)
- Only owner can remove his video or reactions (like,dislike,comment)
- Like and Dislike are mutually exclusive
- A single API to add or remove Like and Dislike to reduce frontend dependency
- to explore more run the projects by following instructions in 'Setup" sections and browsing APIs from three different docs (Links are provided in API section) 

## Setup
```
source venv/bin/activate
pip install -r requirements.txt
source venv/bin/activate
uvicorn videos.main:app --reload --host 0.0.0.0 --port 8002
uvicorn reactions.main:app --reload --host 0.0.0.0 --port 8003
uvicorn users.main:app --reload --host 0.0.0.0 --port 8000
```

### docs
- videos:http://127.0.0.1:8002/videos/docs
- users:http://127.0.0.1:8000/users/docs
- reactions:http://127.0.0.1:8003/reactions/docs