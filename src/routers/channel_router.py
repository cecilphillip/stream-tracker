from fastapi import Response, status, Depends
from fastapi.routing import APIRouter
from motor.motor_asyncio import AsyncIOMotorCollection

from models.channel import Channel
from data.mongo_data import get_channel_collection

channel_router = APIRouter(
    prefix="/channels"
)


@channel_router.get("/")
async def get_channels(skip: int = 0, take: int = 10, collection: AsyncIOMotorCollection = Depends(get_channel_collection)):
    # channel_collection = mongo_data.get_collection('channel')

    results = []
    async for channel in collection.find({}).skip(skip).limit(take):
        results.append(
            Channel(**channel)
        )

    return results


@channel_router.post("/")
async def add_channel(channel: Channel, response: Response):
    """
    /channels handler for adding a new Channel
    """

    mongo_collection = mongo_data.get_collection('channel')
    result = await mongo_collection.insert_one(channel.dict())
    response.status_code = status.HTTP_201_CREATED
    return response
