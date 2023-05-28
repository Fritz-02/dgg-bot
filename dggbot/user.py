import dataclasses
from datetime import datetime


@dataclasses.dataclass
class User:
    id: int
    name: str
    created_date: datetime
    features: list = dataclasses.field(default_factory=list)
