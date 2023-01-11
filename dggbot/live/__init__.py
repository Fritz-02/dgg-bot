import json
from typing import Callable
import websocket
from .message import StreamInfo, YoutubeVideo, YoutubeVod
from .._logging import _logger
from ..funcs import threaded


class DGGLive:
    WSS = "wss://live.destiny.gg/ws"
    ORIGIN = "https://www.destiny.gg"

    def __init__(self, auth_token=None, wss: str = None):
        self.ws = websocket.WebSocketApp(
            wss or self.WSS,
            cookie=f"authtoken={auth_token}" if auth_token else None,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._live = False
        self._connected = False
        self._events = {}

    def __repr__(self):
        return f"{self.__class__.__name__}(live='{self.is_live}')"

    def is_live(self) -> bool:
        return self._live

    def set_live(self, state: bool):
        if not self.is_live() and state:
            self._live = state
            self.on_stream_start()
        elif self.is_live() and not state:
            self._live = state
            self.on_stream_end()

    def _on_message(self, ws, message: str):
        data = json.loads(message)
        if (t := data["type"]) == "dggApi:streamInfo":
            streaminfo = StreamInfo.from_json(data)
            self.set_live(streaminfo.live)
            self.on_streaminfo(streaminfo)
        elif t == "dggApi:youtubeVideos":
            self.on_youtubevideos(YoutubeVideo.from_json(data))
        elif t == "dggApi:youtubeVods":
            self.on_youtubevods(YoutubeVod.from_json(data))
        else:
            _logger.warning(f"Unknown event type: {t} {data}")

    def _on_open(self, ws):
        _logger.debug(f"Connecting to {self.WSS}.")
        self._connected = True

    def _on_close(self, ws, *_):
        _logger.debug(f"Connection closed.")
        self._connected = False

    def _on_error(self, ws, error):
        _logger.error(error)

    def event(self, event_name: str = None):
        """Decorator to run function when the specified event occurs."""

        def decorator(func: Callable):
            event = event_name or func.__name__
            if event not in self._events:
                self._events[event] = []
            self._events[event].append(func)
            return func

        return decorator

    @threaded
    def on_stream_start(self):
        """Do stuff when stream starts."""
        for func in self._events.get("on_stream_start", tuple()):
            func()

    @threaded
    def on_stream_end(self):
        """Do stuff when stream ends."""
        for func in self._events.get("on_stream_end", tuple()):
            func()

    @threaded
    def on_streaminfo(self, streaminfo: StreamInfo):
        """Do stuff when dggApi:streamInfo received."""
        for func in self._events.get("on_streaminfo", tuple()):
            func(streaminfo)

    @threaded
    def on_youtubevideos(self, videos: tuple[YoutubeVideo]):
        """Do stuff when dggApi:youtubeVideos received."""
        for func in self._events.get("on_youtubevideos", tuple()):
            func(videos)

    @threaded
    def on_youtubevods(self, vods: tuple[YoutubeVod]):
        """Do stuff when dggApi:youtubeVods received."""
        for func in self._events.get("on_youtubevods", tuple()):
            func(vods)

    def run(self, origin: str = None):
        self.ws.run_forever(origin=origin or self.ORIGIN)
