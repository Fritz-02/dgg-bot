import dataclasses


@dataclasses.dataclass
class User:
    name: str
    features: list = dataclasses.field(default_factory=list)
