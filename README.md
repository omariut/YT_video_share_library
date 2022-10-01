# YT_video_share_library
This is a YT video share library. User needs to enter YT url of the video, he/she wants to share. Every video has reaction panel where user can like,dislike a video.
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
- reactions:http://127.0.0.1:8002/reactions/docs