import dataclasses


@dataclasses.dataclass
class StreamInfo:
    live: bool
    game: str
    preview: str
    status_text: str
    started_at: str
    ended_at: str
    duration: int
    viewers: int
    id: str

    @classmethod
    def from_json(cls, data: dict) -> "StreamInfo":
        yt = data["data"]["streams"]["youtube"]
        del yt["platform"]
        del yt["type"]
        return cls(**yt)


@dataclasses.dataclass
class YoutubeVideo:
    id: str
    title: str
    mediumThumbnailUrl: str
    highThumbnailUrl: str
    url: str

    @classmethod
    def from_json(cls, data: dict) -> tuple["YoutubeVideo"]:
        return tuple(
            cls(
                vid["id"],
                vid["title"],
                vid["mediumThumbnailUrl"],
                vid["highThumbnailUrl"],
                vid["url"],
            )
            for vid in data["data"]
        )


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
