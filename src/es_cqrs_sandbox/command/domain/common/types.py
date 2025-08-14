from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import NewType, Protocol, Self, runtime_checkable

import uuid6


@runtime_checkable
class Id(Protocol):
    @property
    def value(self) -> str: ...

    @classmethod
    def new(cls) -> Self: ...


@dataclass(slots=True, frozen=True)
class EventId:
    value: str

    @classmethod
    def new(cls) -> Self:
        return cls(value=str(uuid6.uuid7()))


@dataclass(slots=True, frozen=True)
class EventMetadata[T: Id]:
    event_id: EventId
    """イベントの識別子。時系列と分散ユニーク性を確保。"""
    aggregate_id: T
    """集約キー。1ホールドの論理ID。downcast することでこのイベントがどの集約に帰属するかを特定可能。"""
    seq: int
    """楽観ロック用。イベントの発生とともに単調増加。"""
    occurred_at: datetime
    """イベント発生時刻。"""


@runtime_checkable
class Event[T: Id](Protocol):
    @property
    def metadata(self) -> EventMetadata[T]: ...
