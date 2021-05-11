import os
import re
from pprint import pprint
from datetime import datetime, timedelta, timezone
from twitchAPI.twitch import Twitch, VideoType
from dotenv import load_dotenv

from channel import Channel, Stream

load_dotenv("local.env")

twitch_key = os.getenv("TWITCH_CLIENT_KEY")
twitch_id = os.getenv("TWITCH_CLIENT_ID")
twitch_client = Twitch(twitch_id, twitch_key)


def main():
    md_user = twitch_client.get_users(logins=["DashDucks"])
    md_user_id = md_user["data"][0]["id"]

    results = twitch_client.get_videos(
        user_id=md_user_id, video_type=VideoType.ARCHIVE)

    ch = Channel(
        identifier=md_user_id,
        name=md_user["data"][0]["display_name"],
        platform="Twitch"
    )

    hours_pattern = re.compile(r'\d{1,2}(?=h)')
    minutes_pattern = re.compile(r'\d{1,2}(?=m)')
    seconds_pattern = re.compile(r'\d{1,2}(?=s)')

    for vid in results["data"]:
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
        ch.streams.append(stream)

    pprint(ch)


if __name__ == "__main__":
    main()
