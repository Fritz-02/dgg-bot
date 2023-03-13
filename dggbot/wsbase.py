from abc import abstractmethod, ABC
import json
import time
from typing import Callable, Union
import websocket

from .funcs import threaded
from ._logging import _logger


class WSBase(ABC):
    _CONFIG = {
        "wss": "wss://chat.destiny.gg/ws",
        "wss-origin": "https://www.destiny.gg",
    }

    def __init__(
        self,
        wss: str = None,
        cookie: str = None,
        *,
        config: Union[str, dict[str, dict]] = None,
        **kwargs,
    ):
        if isinstance(config, str):
            with open(config) as f:
                self.config = json.load(f)
        elif config is not None:
            self.config = config
        else:
            self.config = self._CONFIG
        self.wss = wss or self.config["wss"]
        self.ws = websocket.WebSocketApp(
            self.wss,
            cookie=cookie,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._connected = False
        self._events = {}

    def __repr__(self):
        return f"{self.__class__.__name__}()"

    # Event methods
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
    def on_event(self, event: str, *args, **kwargs):
        for func in self._events.get(f"on_{event}", tuple()):
            func(*args, **kwargs)

    # Run methods
    def run(self, origin: str = None):
        self.ws.run_forever(origin=origin or self.config["wss-origin"])

    def run_forever(self, origin: str = None, sleep: int = 2):
        """Runs the client forever by automatically reconnecting the websocket."""
        while True:
            self.run(origin=origin or self.config["wss-origin"])
            time.sleep(sleep)

    # Websocket methods
    @abstractmethod
    def _on_message(self, ws, message: str):
        ...

    def _on_open(self, ws):
        _logger.info(f"Connecting to {self.wss}.")
        self._connected = True

    def _on_error(self, ws, error):
        _logger.error(error)

    def _on_close(self, ws, *_):
        _logger.debug(f"Connection closed.")
        self._connected = False
