from datetime import datetime, timezone
import json
import requests
from typing import Union

from ._logging import _logger
from .event import EventType
from .flairs import Flair, flair_converter, convert_flairs
from .funcs import threaded
from .message import (
    Message,
    MuteMessage,
    PinnedMessage,
    PollMessage,
    PrivateMessage,
    VoteMessage,
)
from .user import User
from .wsbase import WSBase
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


class DGGChat(WSBase):
    _CONFIG = {
        "wss": "wss://chat.destiny.gg/ws",
        "wss-origin": "https://www.destiny.gg",
        "baseurl": "https://www.destiny.gg",
        "endpoints": {"user": "/api/chat/me", "userinfo": "/api/userinfo"},
        "flairs": "https://cdn.destiny.gg/flairs/flairs.json",
    }

    def __init__(
        self,
        auth_token=None,
        wss: str = None,
        *,
        sid: str = None,
        rememberme: str = None,
        config: Union[str, dict[str, dict]] = None,
        **kwargs,
    ):
        cookie = (
            f"authtoken={auth_token}"
            if auth_token
            else (
                f"sid={sid}" + (f";rememberme={rememberme}" if rememberme else "")
                if sid
                else None
            )
        )
        super().__init__(wss, cookie, config=config)
        self.user = None
        self._flairs = flair_converter(self.config["flairs"])
        self.authenticated = False
        self._users = {}

    @property
    def username(self) -> str:
        if self.user is not None:
            return self.user.name

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(username='{self.username}')"
            if self.username
            else f"{self.__class__.__name__}()"
        )

    # The following two functions are probably pointless now with the ME event, but I'll leave them in for now. - Fritz
    def _get_username_from_token(self, auth_token: str) -> Union[str, None]:
        r = requests.get(
            f"{self.config['baseurl']}{self.config['endpoints']['userinfo']}?token={auth_token}"
        )
        resp = r.json()
        if "username" in resp:
            return resp["username"].lower()
        else:
            _logger.error(
                f"Could not get username from token: {resp.get('message', 'Unknown reason.')}"
            )

    def _get_username_from_sid(self, cookie: str) -> Union[str, None]:
        headers = {"cookie": cookie}
        r = requests.get(
            self.config["baseurl"] + self.config["endpoints"]["user"],
            headers=headers,
        )
        resp = r.json()
        if r.status_code == 200:
            resp = r.json()
            return resp["nick"].lower()
        else:
            _logger.error(
                f"Authentication failed. Error {resp['code']}: {resp['error']}"
            )

    @property
    def users(self) -> dict:
        return self._users.copy()

    def get_user(self, username: str) -> Union[User, None]:
        return self._users.get(username.lower())

    def get_flair(self, name: str) -> Flair:
        return self._flairs[name]

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
        if event_type == EventType.ME:
            _logger.debug(f"{event_type} {data}")
            if data is not None:
                self.user = User(
                    data["id"],
                    data["nick"],
                    convert_flairs(self._flairs, data.get("features")),
                )
            else:
                self.user = None
            return
        elif event_type == EventType.MUTE:
            msg = MuteMessage(self, event_type, data)
        elif event_type == EventType.PRIVMSG:
            msg = PrivateMessage(self, event_type, data)
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
        elif event_type == EventType.PIN:
            msg = PinnedMessage(self, event_type, data)
        elif event_type in (EventType.POLLSTART, EventType.POLLSTOP):
            msg = PollMessage(self, event_type, data)
        elif event_type == EventType.VOTECAST:
            msg = VoteMessage(self, event_type, data)
        else:
            msg = Message(self, event_type, data)
        if event_type == EventType.QUIT:
            self._users.pop(msg.nick_lower, None)
        elif event_type == EventType.JOIN:
            self._users[msg.nick_lower] = msg.user

        self.on_event(event_type.lower(), msg)
        if event_type in (EventType.MESSAGE, EventType.PRIVMSG) and self.is_mentioned(
            msg
        ):
            self.on_event("mention", msg)
        self._post_message(msg)

    def _post_message(self, msg):
        """Do stuff after _on_message"""
        pass

    def _on_open(self, ws):
        _logger.info(
            f"Connecting "
            + (f"as {self.username} " if self.username else "")
            + f"to {self.wss}."
        )
        self._connected = True

    def mention(self):
        """Decorator to run function on mentions. Shortcut for event('on_mention')."""
        return self.event("on_mention")

    def is_mentioned(self, msg: Union[Message, PrivateMessage]) -> bool:
        return (
            False if self.username is None else (self.username in msg.data.casefold())
        )

    @threaded
    def on_names(self, connection_count: int, users: list):
        """Do stuff when the NAMES message is received upon connecting to chat."""
        self._users = {
            user["nick"].lower(): User(
                user.get("id"),
                user.get("nick"),
                convert_flairs(self._flairs, user.get("features")),
            )
            for user in users
        }
        self.on_event("names", connection_count, self._users)

    @threaded
    def send_raw(self, event_type: str, payload: dict):
        """Send the specified event_type and payload."""
        self.ws.send(f"{event_type} {json.dumps(payload)}")

    @threaded
    def send(self, msg: str):
        """Send a message to chat."""
        assert len(msg) <= 512, "512 character limit broken"
        payload = {"data": msg}
        self.ws.send(f"MSG {json.dumps(payload)}")

    @threaded
    def send_privmsg(self, nick: str, msg: str):
        """Send private message to someone."""
        payload = {"nick": nick, "data": msg}
        self.ws.send(f"PRIVMSG {json.dumps(payload)}")

    @threaded
    def cast_vote(self, vote: int):
        """Participate in a chat poll."""
        payload = {"vote": str(vote)}
        self.ws.send(f"CASTVOTE {json.dumps(payload)}")
