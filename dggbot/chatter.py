import dataclasses


@dataclasses.dataclass
class Chatter:
    name: str
    features: list = dataclasses.field(default_factory=list)
