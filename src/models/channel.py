from pydantic import BaseModel

class Channel(BaseModel):   
    channel_id: int
    channel_name: str
    platform: str # mostly Twtich
    url: str
