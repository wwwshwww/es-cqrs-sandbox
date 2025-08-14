from dataclasses import dataclass
from typing import NewType, Self

from uuid6 import uuid7


@dataclass(slots=True, frozen=True)
class UserId:
    value: str

    @classmethod
    def new(cls) -> Self:
        return cls(value=str(uuid7()))
