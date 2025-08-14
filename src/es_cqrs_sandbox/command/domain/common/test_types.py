import datetime
import uuid
from dataclasses import dataclass
from typing import Self

import uuid6

from .types import Event, EventId, EventMetadata

# --- aggregate sample 1 ---


@dataclass(slots=True, frozen=True)
class MyId:
    value: str

    @classmethod
    def new(cls) -> Self:
        return cls(value=str(uuid6.uuid7()))


@dataclass(slots=True, frozen=True)
class MyEventV1:
    metadata: EventMetadata[MyId]

    a: int


@dataclass(slots=True, frozen=True)
class MyEventV2:
    metadata: EventMetadata[MyId]

    a: int
    b: int


# --- aggregate sample 2 ---


@dataclass(slots=True, frozen=True)
class YourId:
    value: str

    @classmethod
    def new(cls) -> Self:
        return cls(value=str(uuid.uuid4()))


@dataclass(slots=True, frozen=True)
class YourEventV1:
    metadata: EventMetadata[YourId]

    c: str


# ----------------------------


def do_something(x: Event[MyId] | Event[YourId]) -> None:
    print(x.metadata.aggregate_id)


def test_impl_example():
    do_something(
        MyEventV1(
            metadata=EventMetadata(
                event_id=EventId.new(),
                aggregate_id=MyId.new(),
                seq=1,
                occurred_at=datetime.now(),
            ),
            a=0,
        )
    )

    do_something(
        MyEventV2(
            metadata=EventMetadata(
                event_id=EventId.new(),
                aggregate_id=MyId.new(),
                seq=1,
                occurred_at=datetime.now(),
            ),
            a=0,
            b=0,
        )
    )

    do_something(
        YourEventV1(
            metadata=EventMetadata(
                event_id=EventId.new(),
                aggregate_id=YourId.new(),
                seq=1,
                occurred_at=datetime.now(),
            ),
            c="Bob",
        )
    )
