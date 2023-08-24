from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING, Union

from ._logging import _logger
from .flairs import Flair, convert_flairs
from .user import User

if TYPE_CHECKING:
    from .chat import DGGChat


def convert_datetime(dt_string: Union[str, None]) -> Union[datetime, None]:
    if dt_string is None:
        return
    if (n := len(dt_string)) == 20:  # seconds given
        dt = datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%SZ")
    elif n <= 27:  # microseconds given
        dt = datetime.strptime(dt_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:  # if more than 6 digits for microseconds is given, do not include them. Datetime only allows up to 6
        dt = datetime.strptime(dt_string[:26] + "Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt


def convert_timestamp(ts: Union[int, None]) -> Union[datetime, None]:
    """ts: timestamp (in microseconds)"""
    if ts is None:
        return
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
    def nick_lower(self) -> Union[str, None]:
        if self.nick:
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
        self.created_date = convert_datetime(data.get("createdDate"))
        self.timestamp = convert_timestamp(data.get("timestamp"))
        self.data: str = data.get("data")

    @property
    def user(self) -> User:
        return User(self.id, self.nick, self.created_date, self.features)

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


class BroadcastMessage(_MessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.data: str = data.get("data")


class _SubMessageBase(_MessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.timestamp = convert_timestamp(data.get("timestamp"))
        self.data: str = data.get("data")
        self.tier: int = data.get("tier")
        self.tier_label: str = data.get("tierLabel")


class SubscriptionMessage(_SubMessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.streak: int = data.get("streak")


class MassGiftMessage(_SubMessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.quantity: int = data.get("quantity")


class GiftSubMessage(_SubMessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.giftee: int = data.get("giftee")


class DonationMessage(_MessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.timestamp = convert_timestamp(data.get("timestamp"))
        self.data: str = data.get("data")
        self.amount: int = data.get("amount")  # in US cents


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

    def vote(self, option: int):
        self.chat.cast_vote(option)


class VoteMessage(_MessageBase):
    def __init__(self, chat: DGGChat, type_: str, data: dict):
        super().__init__(chat, type_, data)
        self.vote: str = data.get("vote")
