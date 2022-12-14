from fastapi import FastAPI, APIRouter, Depends
from reactions.api.routers.likes import likes
from reactions.api.routers.dislikes import dislikes
from reactions.api.routers.comments import comments
from reactions.api.user import users
from reactions.api.db import metadata, database, engine


metadata.create_all(engine)

app = FastAPI(openapi_url="/reactions/openapi.json", docs_url="/reactions/docs")


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(users)
app.include_router(likes, prefix="/likes", tags=["likes"])
app.include_router(dislikes, prefix="/dislikes", tags=["dislikes"])
app.include_router(comments, prefix="/comments", tags=["comments"])
