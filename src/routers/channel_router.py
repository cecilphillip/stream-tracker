from fastapi import Response, status
from fastapi.routing import APIRouter

from models.channel import Channel
from data import mongo_data

channel_router = APIRouter(
    prefix="/channels"
)

@channel_router.get("/")
async def get_channels():
    channel_collection = mongo_data.get_collection('channel')

    results = []
    async for channel in channel_collection.find({}):
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
