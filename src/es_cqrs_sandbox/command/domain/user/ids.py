from dataclasses import dataclass
from typing import NewType, Self
from uuid import UUID

from uuid6 import uuid7


@dataclass(slots=True, frozen=True)
class UserId:
    value: UUID

    @classmethod
    def new(cls) -> Self:
        return cls(value=uuid7())
