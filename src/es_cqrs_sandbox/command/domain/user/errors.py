from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Error(Protocol):
    message: str


@dataclass(frozen=True)
class InvalidOperationError(Error):
    message: str
