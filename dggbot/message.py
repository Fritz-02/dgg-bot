import dataclasses
from ._logging import _logger


@dataclasses.dataclass
class Message:
    chat: "DGGChat"
    type: str
    nick: str = None
    features: list = None
    timestamp: int = None
    data: str = None

    @property
    def nick_lower(self) -> str:
        return self.nick.lower()

    def __post_init__(self):
        _logger.debug(self)

    def reply(self, content):
        self.chat.send(content)


@dataclasses.dataclass
class PrivateMessage(Message):
    message_id: str = None

    def reply(self, content):
        self.chat.send_privmsg(self.nick, content)


@dataclasses.dataclass
class MuteMessage(Message):
    duration: int = None
