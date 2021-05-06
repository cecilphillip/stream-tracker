from data.mongo_data import get_channel_collection
from models.channel import Channel

async def get_channel_records(skip: int, take: int):
    collection = get_channel_collection()
    
    results = []
    
    async for channel in collection.find({}).skip(skip).limit(take):
        results.append(
            Channel(**channel)
        )
    return results
    