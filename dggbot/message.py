import dataclasses
from datetime import datetime
from ._logging import _logger
from .user import User


@dataclasses.dataclass
class _MessageBase:
    chat: "DGGChat"
    type: str
    nick: str = None

    @property
    def nick_lower(self) -> str:
        return self.nick.lower()

    def __post_init__(self):
        _logger.debug(self)


@dataclasses.dataclass
class Message(_MessageBase):
    createdDate: datetime = None
    features: list = None
    timestamp: datetime = None
    data: str = None

    @property
    def user(self) -> User:
        return User(self.nick, self.createdDate, self.features)

    def reply(self, content):
        self.chat.send(content)


@dataclasses.dataclass
class MuteMessage(Message):
    duration: int = None


@dataclasses.dataclass
class PinnedMessage(Message):
    uuid: str = None


@dataclasses.dataclass
class PrivateMessage(Message):
    message_id: str = None

    def reply(self, content):
        self.chat.send_privmsg(self.nick, content)
