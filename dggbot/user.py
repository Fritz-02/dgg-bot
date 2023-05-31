from __future__ import annotations

import dataclasses
import re
from datetime import datetime
from functools import cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message


@dataclasses.dataclass
class User:
    id: int
    name: str
    created_date: datetime
    features: list = dataclasses.field(default_factory=list)

    @cache
    def _name_regex(self) -> re.Pattern:
        return re.compile(rf"\b{self.name}\b", re.IGNORECASE)

    def is_mentioned(self, msg: Message) -> bool:
        return bool(self._name_regex().search(msg.data))

    def __hash__(self):
        return hash((self.id, self.name, self.created_date, tuple(self.features)))
