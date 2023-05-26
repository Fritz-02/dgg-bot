from __future__ import annotations

from datetime import datetime, timezone
from ._logging import _logger
from .flairs import Flair, convert_flairs
from .user import User

from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from .chat import DGGChat


def convert_datetime(dt_string: str) -> datetime:
    # DGG returns a string with 9 microsecond digits, while datetime only goes up to 6. So the last 3 are cut off.
    dt = datetime.strptime(f"{dt_string[:-4]}Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt


def convert_timestamp(ts: int) -> datetime:
    """ts: timestamp (in microseconds)"""
    return datetime.fromtimestamp(ts // 1000, tz=timezone.utc)


class _MessageBase:
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        self.chat = chat
        self.type = type_
        self.nick: str = data.get("nick")
        self._data = data

    def get(self, key: str):
        return self._data.get(key)

    @property
    def nick_lower(self) -> str:
        return self.nick.lower()

    def __post_init__(self):
        _logger.debug(self)

    def __repr__(self):
        return (
            f"""{self.__class__.__name__}"""
            + f"""({', '.join([f"{k}={repr(v)}" for k, v in self.__dict__.items() if k != '_data'])})"""
        )


class Message(_MessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.id: int = data.get("ID")
        self.features: list[Flair] = convert_flairs(chat._flairs, data.get("features"))
        self.last_message: str = data.get("Lastmessage")
        self.last_message_time: datetime = convert_datetime(data.get("Lastmessagetime"))
        self.delay_scale: int = data.get("Delayscale")
        self.connections: int = data.get("Connections")
        self.timestamp = convert_timestamp(data.get("timestamp"))
        self.data: str = data.get("data")

    @property
    def user(self) -> User:
        return User(self.id, self.nick, self.features)

    def reply(self, content):
        self.chat.send(content)


class MuteMessage(Message):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.duration: int = data.get("duration")


class PrivateMessage(_MessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.message_id: int = data.get("messageid")
        self.timestamp: datetime = convert_timestamp(data.get("timestamp"))
        self.data: str = data.get("data")

    @property
    def user(self) -> User:
        return self.chat.get_user(self.nick)

    def reply(self, content):
        self.chat.send_privmsg(self.nick, content)


class PinnedMessage(Message):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.uuid: str = data.get("uuid")


class PollMessage(_MessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.can_vote: bool = data.get("canvote")
        self.my_vote: int = data.get("myvote")
        self.weighted: bool = data.get("weighted")
        self.start: datetime = convert_datetime(data.get("start"))
        self.now: datetime = convert_datetime(data.get("now"))
        self.time: int = data.get("time")
        self.question: str = data.get("question")
        self.options: list[str] = data.get("options")
        self.totals: list[int] = data.get("totals")
        self.total_votes: int = data.get("totalvotes")


class VoteMessage(_MessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.vote: str = data.get("vote")
