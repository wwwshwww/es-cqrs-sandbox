from dataclasses import dataclass
from datetime import datetime
from typing import Protocol


@dataclass(frozen=True)
class Metadata[T]:
    entity_id: T
    seq: int
    timestamp: datetime


@dataclass(frozen=True)
class Event[T](Protocol):
    metadata: Metadata[T]
