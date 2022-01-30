import dataclasses


@dataclasses.dataclass
class Message:
    type: str
    nick: str = None
    features: list = None
    timestamp: int = None
    data: str = None


@dataclasses.dataclass
class PrivateMessage:
    type: str
    nick: str = None
    timestamp: int = None
    data: str = None
    message_id: str = None



