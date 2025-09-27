from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Self, runtime_checkable
from uuid import UUID, uuid4

from uuid6 import uuid7


class Id(Protocol):
    @classmethod
    def new(cls) -> Self: ...


@dataclass(frozen=True, slots=True)
class EventId:
    value: UUID

    @classmethod
    def new(cls) -> EventId:
        return EventId(uuid7())


@runtime_checkable
class EventPayload[T: Id](Protocol):
    @property
    def aggregate_id(self) -> T:
        """集約キー。1ホールドの論理ID。downcast するとこのイベントがどの集約に帰属するかを特定可能。"""
        ...


@dataclass(slots=True, frozen=True)
class Event[T: EventPayload[Id]]:
    id_: EventId
    """イベントの識別子。時系列と分散ユニーク性を確保。"""
    seq: int
    """楽観ロック用。イベントの発生とともに単調増加。"""
    occurred_at: datetime
    """イベント発生時刻。"""

    payload: T
    """イベントの中身。"""

    @classmethod
    def new[U: EventPayload[Id]](
        cls, seq: int, occurred_at: datetime, payload: U
    ) -> Event[U]:
        return Event(
            id_=EventId.new(),
            seq=seq,
            occurred_at=occurred_at,
            payload=payload,
        )

    def next_seq(self) -> int:
        return self.seq + 1
