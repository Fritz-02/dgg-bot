from datetime import datetime, timezone
import json
from typing import Callable, Union
import websocket

from .event import EventType
from ._logging import _logger
from .funcs import threaded
from .message import Message, PrivateMessage, MuteMessage
from .user import User
from .errors import (
    AccountTooYoung,
    Banned,
    DuplicateMessage,
    InvalidMessage,
    NeedLogin,
    NoPermission,
    NotFound,
    ProtocolError,
    SubMode,
    Throttled,
    TooManyConnections,
)


class DGGChat:
    WSS = "wss://chat.destiny.gg/ws"
    URL = "https://www.destiny.gg"

    def __init__(self, auth_token=None, username: str = None, wss: str = None):
        self.username = username.lower() if isinstance(username, str) else None
        self.wss = wss or self.WSS
        self.ws = websocket.WebSocketApp(
            self.wss,
            cookie=f"authtoken={auth_token}" if auth_token else None,
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
        )
        self._connected = False
        self._events = {}
        self._users = {}

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(username='{self.username}')"
            if self.username
            else f"{self.__class__.__name__}()"
        )

    def _dggtime_to_dt(self, timestamp: str) -> datetime:
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

    def _dggepoch_to_dt(self, epoch: int) -> datetime:
        return datetime.fromtimestamp(epoch // 1000, tz=timezone.utc)  # dgg sends miliseconds

    @property
    def users(self) -> dict:
        return self._users.copy()

    def get_user(self, username: str) -> Union[User, None]:
        return self._users.get(username.lower())

    _err_dict = {
        "banned": Banned,
        "duplicate": DuplicateMessage,
        "invalidmsg": InvalidMessage,
        "needlogin": NeedLogin,
        "nopermission": NoPermission,
        "notfound": NotFound,
        "privmsgaccounttooyoung": AccountTooYoung,
        "protocolerror": ProtocolError,
        "submode": SubMode,
        "throttled": Throttled,
        "toomanyconnections": TooManyConnections,
    }

    def _on_message(self, ws, message: str):
        event_type, data = message.split(maxsplit=1)
        data = json.loads(data)
        if event_type == EventType.MUTE:
            msg = MuteMessage(
                self,
                event_type,
                data["nick"],
                self._dggtime_to_dt(data["createdDate"]),
                data["features"],
                self._dggepoch_to_dt(data["timestamp"]),
                data["data"],
                data["duration"],
            )
        elif event_type == EventType.BROADCAST:
            msg = Message(
                self, event_type, timestamp=self._dggepoch_to_dt(data["timestamp"]), data=data["data"]
            )
        elif event_type == EventType.PRIVMSG:
            msg = PrivateMessage(
                self,
                event_type,
                data["nick"],
                timestamp=self._dggepoch_to_dt(data["timestamp"]),
                data=data["data"],
                message_id=data["messageid"],
            )
        elif event_type == EventType.PRIVMSGSENT:
            return
        elif event_type == EventType.ERROR:
            if (desc := data["description"]) in self._err_dict:
                raise self._err_dict[desc]
            else:
                _logger.error(event_type, data)
                raise Exception(desc)
        elif event_type == EventType.NAMES:
            _logger.debug(f"{event_type} {data}")
            self.on_names(data["connectioncount"], data["users"])
            return
        elif event_type in (EventType.MESSAGE,
                            EventType.UNMUTE,
                            EventType.BAN,
                            EventType.UNBAN,
                            EventType.SUBONLY,
                            EventType.BROADCAST,
                            EventType.JOIN,
                            EventType.QUIT,
                            EventType.REFRESH):
            msg = Message(
                self,
                event_type,
                data["nick"],
                self._dggtime_to_dt(data["createdDate"]),
                data["features"],
                self._dggepoch_to_dt(data["timestamp"]),
                data.get("data"),
            )
        else:
            _logger.warning(f"Unknown event type: {event_type} {data}")
            return
        func_name = f"on_{event_type.lower()}"
        if hasattr(self, func_name):
            f = getattr(self, func_name)
            f(msg)
        else:
            _logger.warning(f"Function '{func_name}' not found.")
        if event_type in (EventType.MESSAGE, EventType.PRIVMSG):
            if self.is_mentioned(msg):
                self.on_mention(msg)

    def _on_open(self, ws):
        _logger.debug(
            f"Connecting "
            + (f"as {self.username} " if self.username else "")
            + f"to {self.wss}."
        )
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

    def mention(self):
        """Decorator to run function on mentions. Shortcut for event('on_mention')."""
        return self.event("on_mention")

    def is_mentioned(self, msg: Union[Message, PrivateMessage]) -> bool:
        return (
            False if self.username is None else (self.username in msg.data.casefold())
        )

    @threaded
    def on_mention(self, msg):
        """Do stuff when mentioned."""
        for func in self._events.get("on_mention", tuple()):
            func(msg)

    @threaded
    def on_msg(self, msg: Message):
        """Do stuff when a MSG is received."""
        for func in self._events.get("on_msg", tuple()):
            func(msg)

    @threaded
    def on_names(self, connection_count: int, users: list):
        """Do stuff when the NAMES message is received upon connecting to chat."""
        self._users = {
            user["nick"].lower(): User(user["nick"], self._dggtime_to_dt(user["createdDate"]), user["features"]) for user in users
        }
        for func in self._events.get("on_names", tuple()):
            func(connection_count, users)

    @threaded
    def on_privmsg(self, msg: PrivateMessage):
        """Do stuff when a PRIVMSG is received."""
        for func in self._events.get("on_privmsg", tuple()):
            func(msg)

    def run(self, origin: str = None):
        self.ws.run_forever(origin=origin or self.URL)

    @threaded
    def send(self, msg: str):
        """Send a message to chat."""
        payload = {"data": msg}
        self.ws.send(f"MSG {json.dumps(payload)}")

    @threaded
    def send_privmsg(self, nick: str, msg: str):
        """Send private message to someone."""
        payload = {"nick": nick, "data": msg}
        self.ws.send(f"PRIVMSG {json.dumps(payload)}")

    @threaded
    def on_broadcast(self, msg):
        """Do stuff when a BROADCAST is received."""
        for func in self._events.get("on_broadcast", tuple()):
            func(msg)

    @threaded
    def on_join(self, msg: Message):
        """Do stuff when chatter joins."""
        self._users[msg.nick_lower] = User(msg.nick, msg.createdDate, msg.features)
        for func in self._events.get("on_join", tuple()):
            func(msg)

    @threaded
    def on_quit(self, msg):
        """Do stuff when chatter joins."""
        self._users.pop(msg.nick_lower)
        for func in self._events.get("on_quit", tuple()):
            func(msg)

    @threaded
    def on_ban(self, msg: Message):
        """Do stuff when a chatter is banned."""
        for func in self._events.get("on_ban", tuple()):
            func(msg)

    @threaded
    def on_unban(self, msg: Message):
        """Do stuff when a chatter is unbanned."""
        for func in self._events.get("on_unban", tuple()):
            func(msg)

    @threaded
    def on_mute(self, msg: MuteMessage):
        """Do stuff when a chatter is muted."""
        for func in self._events.get("on_mute", tuple()):
            func(msg)

    @threaded
    def on_unmute(self, msg: Message):
        """Do stuff when a chatter is unmuted."""
        for func in self._events.get("on_unmute", tuple()):
            func(msg)

    @threaded
    def on_subonly(self, msg: Message):
        """Do stuff when sub-only is turned on/off."""
        for func in self._events.get("on_subonly", tuple()):
            func(msg)

    @threaded
    def on_refresh(self, msg: Message):
        """Do stuff when refreshed."""
        for func in self._events.get("on_refresh", tuple()):
            func(msg)
