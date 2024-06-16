import json
from typing import Union

from .._logging import _logger
from ..wsbase import WSBase
from .message import Embed, Stream, StreamInfo, YoutubeVideo, YoutubeVod


class DGGLive(WSBase):
    _CONFIG = {
        "wss": "wss://live.destiny.gg/",
        "wss-origin": "https://www.destiny.gg",
    }

    def __init__(
        self,
        auth_token=None,
        wss: str = None,
        *,
        config: Union[str, dict[str, dict]] = None,
    ):
        super().__init__(
            wss, f"authtoken={auth_token}" if auth_token else None, config=config
        )
        self._live = False

    def __repr__(self):
        return f"{self.__class__.__name__}(live='{self.is_live}')"

    def is_live(self) -> bool:
        return self._live

    def set_live(self, state: bool):
        if not self.is_live() and state:
            self._live = state
            self.on_event("stream_start")
        elif self.is_live() and not state:
            self._live = state
            self.on_event("stream_end")

    def _on_message(self, ws, message: str):
        data = json.loads(message)
        event_type = data["type"]
        event_data = data
        if event_type == "dggApi:hosting":
            event_data = data["data"]
        elif event_type == "dggApi:streamInfo":
            event_data = StreamInfo.from_json(data)
            self.set_live(event_data.is_live())
        elif event_type == "dggApi:videos":
            if (source := event_data["data"]["source"]) == "youtube":
                event_data = YoutubeVideo.from_json(data)
        elif event_type == "dggApi:youtubeVods":
            event_data = YoutubeVod.from_json(data)
        elif event_type == "dggApi:embeds":
            event_data = [Embed.from_json(e) for e in data["data"]]
        self.on_event(event_type.split(":")[-1].lower(), event_data)
