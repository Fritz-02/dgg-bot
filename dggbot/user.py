import dataclasses


@dataclasses.dataclass
class User:
    id: int
    name: str
    features: list = dataclasses.field(default_factory=list)
