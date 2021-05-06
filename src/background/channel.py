from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Stream:
    start_date: datetime
    end_date: datetime
    title: str
    description: str
    tag: list[str] = field(default_factory=list)


@dataclass
class Channel:
    identifier: str
    name: str
    platform: str
    url: str = ""
    last_updated: datetime = field(default_factory=datetime.now)
    streams: list[Stream] = field(default_factory=list)
