from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import NewType, Protocol, Self, runtime_checkable

from uuid6 import UUID


@dataclass(slots=True, frozen=True)
class Metadata[A: UUID]:
    aggregate_id: A
    seq: int
    occurred_at: datetime


@runtime_checkable
class Event[A: UUID](Protocol):
    metadata: Metadata[A]
