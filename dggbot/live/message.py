import dataclasses
from typing import Union


@dataclasses.dataclass
class Stream:
    live: bool
    game: str
    preview: str
    status_text: str
    started_at: str
    ended_at: str
    duration: int
    viewers: int
    id: str
    platform: str
    type: str

    @classmethod
    def from_json(cls, data: dict) -> "Stream":
        return cls(**data)


@dataclasses.dataclass
class StreamInfo:
    twitch: Stream = None
    youtube: Stream = None
    facebook: Stream = None
    rumble: Stream = None
    kick: Stream = None

    def is_live(self) -> bool:
        streams = (
            s
            for s in (self.twitch, self.youtube, self.facebook, self.rumble, self.kick)
            if s is not None
        )
        return any(stream.live for stream in streams)

    def get_livestreams(self) -> tuple[Stream]:
        """Returns streams that are currently live."""
        streams = tuple(s for s in (self.twitch, self.youtube, self.facebook, self.rumble, self.kick) if isinstance(s, Stream) and s.live)
        return streams

    @property
    def viewers(self) -> int:
        """Returns the sum of viewers from each livestream."""
        return sum(s.viewers for s in (self.twitch, self.youtube, self.facebook, self.rumble, self.kick) if isinstance(s, Stream) and s.live)

    @classmethod
    def from_json(cls, data: dict) -> "StreamInfo":
        streams = {
            k: Stream.from_json(v)
            for k, v in data["data"]["streams"].items()
            if v is not None
        }
        return cls(**streams)


@dataclasses.dataclass
class YoutubeVideo:
    id: str
    title: str
    mediumThumbnailUrl: str
    highThumbnailUrl: str
    streamViewers: str
    streamStartTime: str
    streamEndTime: str
    url: str
    thumbnailHref: str

    @classmethod
    def from_json(cls, data: dict) -> tuple["YoutubeVideo"]:
        return tuple(cls(**vid) for vid in data["data"]["videos"])


@dataclasses.dataclass
class YoutubeVod:
    id: str
    title: str
    mediumThumbnailUrl: str
    highThumbnailUrl: str
    streamStartTime: str
    streamEndTime: str
    url: str

    @classmethod
    def from_json(cls, data: dict) -> tuple["YoutubeVod"]:
        return tuple(cls(**vod) for vod in data["data"])
