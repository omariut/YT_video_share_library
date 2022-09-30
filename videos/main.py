from fastapi import FastAPI
from videos.api.videos import videos
from videos.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/videos/openapi.json", docs_url="/videos/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(videos, prefix='/videos/videos', tags=['videos'])

