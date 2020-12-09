# Established: 12/2/2020
from fastapi import FastAPI, Response, status
from http import HTTPStatus
from motor.motor_asyncio import AsyncIOMotorClient
from models.channel import Channel

api = FastAPI()
mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(
    'mongodb://admin:admin@localhost:27017')


@api.on_event("startup")
async def startup():
    pass
   #mongo_client = AsyncIOMotorClient('mongodb://admin:admin@localhost:27017')


@api.on_event("shutdown")
async def shutdown():
    pass
    #mongo_client.close()


@api.post("/addstream")
async def add_stream(response: Response):
    """
    Testing out adding a new document
    """
    channel = Channel(
        channel_id = 1,
        channel_name= "MS Developer",
        platform = "Twitch",
        url = "https://twitch.tv/microsoftdeveloper"
    )

    result = await mongo_client.stream_tracker.channel.insert_one(channel.dict())
    response.status_code = status.HTTP_201_CREATED
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:api")
