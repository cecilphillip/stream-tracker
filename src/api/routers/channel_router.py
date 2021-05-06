from fastapi import Response, status, Depends
from fastapi.routing import APIRouter
from motor.motor_asyncio import AsyncIOMotorCollection

from models.channel import Channel
from data.mongo_data import get_channel_collection

from services.channels_service import get_channel_records

channel_router = APIRouter(
    prefix="/channels"
)


@channel_router.get("")   # /
async def get_channels(skip: int = 0, take: int = 10):
    results = await get_channel_records(skip, take)
    return results


@channel_router.post("")
async def add_channel(channel: Channel, response: Response, collection: AsyncIOMotorCollection = Depends(get_channel_collection)):
    """
    /channels handler for adding a new Channel
    """

    result = await collection.insert_one(channel.dict())
    response.status_code = status.HTTP_201_CREATED
    return response
