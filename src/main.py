# Established: 12/2/2020
from fastapi import FastAPI

from data import mongo_data
from routers.channel_router import channel_router

api = FastAPI()
api.include_router(channel_router)

@api.on_event("startup")
async def startup():
    mongo_data.connect()  # Setup connection to Mongo


@api.on_event("shutdown")
async def shutdown():
    mongo_data.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:api")
