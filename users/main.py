from fastapi import FastAPI
from users.api.users import users
from users.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/users/openapi.json", docs_url="/users/docs")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(users, prefix='/users/users', tags=['users'])

