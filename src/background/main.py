import os
from twitchAPI.twitch import Twitch, VideoType
from dotenv import load_dotenv

from channel import Channel, Stream
import pprint

load_dotenv("local.env")

twitch_key = os.getenv("TWITCH_CLIENT_KEY")
twitch_id = os.getenv("TWITCH_CLIENT_ID")
twitch_client = Twitch(twitch_id, twitch_key)


def main():
    md_user = twitch_client.get_users(logins=["MicrosoftDeveloper"])
    md_user_id = md_user["data"][0]["id"]

    results = twitch_client.get_videos(
        user_id=md_user_id, video_type=VideoType.ARCHIVE)


    ch = Channel(
        identifier=md_user_id,
        name=md_user["data"][0]["display_name"],
        platform="Twitch"
    )

    for vid in results["data"]:
        stream = Stream(
            title=vid["title"],
            description=vid["description"],
            start_date=vid["published_at"]
        )
        ch.streams.append(stream)

    pprint(ch)


if __name__ == "__main__":
    main()
