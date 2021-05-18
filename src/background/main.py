import os
import re
from motor.motor_asyncio import AsyncIOMotorClient
from rich.console import Console
from datetime import datetime, timedelta
from twitchAPI.twitch import Twitch, VideoType
from dotenv import load_dotenv

from channel import Channel, Stream

load_dotenv("local.env")

twitch_key = os.getenv("TWITCH_CLIENT_KEY")
twitch_id = os.getenv("TWITCH_CLIENT_ID") or ""
twitch_client = Twitch(twitch_id, twitch_key)


def get_channels_from_environment() -> list[str]:
    ch_env: str = os.getenv("DEFAULT_TRACKER_CHANNEL_SOURCE") or ""
    return ch_env.split(", ")


def retrieve_streams(user_id: str) -> list[Stream]:

    # get videos for user_id
    # TODO: exception handling at some point
    user_videos = twitch_client.get_videos(
        user_id=user_id, video_type=VideoType.ARCHIVE)

    # create regex patterns to match stream duration
    hours_pattern = re.compile(r'\d{1,2}(?=h)')
    minutes_pattern = re.compile(r'\d{1,2}(?=m)')
    seconds_pattern = re.compile(r'\d{1,2}(?=s)')

    # extract the stream data
    results: list[Stream] = []
    for vid in user_videos["data"]:
        duration = vid["duration"]
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        start_date: datetime = datetime.strptime(
            vid["published_at"], date_format)
        end_date: datetime = start_date

        hours = hours_pattern.search(duration)
        if hours:
            end_date = end_date + timedelta(hours=int(hours.group()))

        minutes = minutes_pattern.search(duration)
        if minutes:
            end_date = end_date + timedelta(minutes=int(minutes.group()))

        seconds = seconds_pattern.search(duration)
        if seconds:
            end_date = end_date + timedelta(seconds=int(seconds.group()))

        stream = Stream(
            title=vid["title"],
            description=vid["description"],
            start_date=start_date,
            end_date=end_date
        )
        results.append(stream)

    return results


def inspect_channels(channel_names: list[str]) -> list[Channel]:
    users = twitch_client.get_users(logins=channel_names)

    channels: list[Channel] = []
    for user in users["data"]:
        user_id = user["id"]

        ch = Channel(
            identifier=user_id,
            name=user["display_name"],
            platform="Twitch"
        )
        ch.streams = retrieve_streams(user_id)
        channels.append(ch)

    return channels


def main():
    # determine channel source
    ch_source = os.getenv("CHANNEL_SOURCE")

    channel_names: list[str] = []
    if ch_source == "environment":
        channel_names = get_channels_from_environment()
    elif ch_source == "database":
        pass

    # mongo_connection_str = os.getenv("MONGO_CONNECTION_STRING") or ""
    # mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(mongo_connection_str)
    # db_name = os.getenv("MONGO_DATABASE_NAME")
    # mdb_channel = mongo_client.get_database(db_name).get_collection("channels")

    channels = inspect_channels(channel_names)
    console = Console()
    console.print(channels)


if __name__ == "__main__":
    main()
