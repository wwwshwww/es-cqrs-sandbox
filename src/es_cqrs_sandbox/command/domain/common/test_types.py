from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from uuid6 import uuid7

from es_cqrs_sandbox.command.domain.common.types import Event, EventId, Id

# --- aggregate sample 1 ---


@dataclass(slots=True, frozen=True)
class MyId(Id):
    value: UUID

    @classmethod
    def new(self) -> MyId:
        return MyId(uuid7())


@dataclass(slots=True, frozen=True)
class MyEvent1:
    aggregate_id: MyId
    value1: str


@dataclass(slots=True, frozen=True)
class MyEvent2:
    aggregate_id: MyId
    value2: str
    value3: str


type MyEvent = Event[MyEvent1] | Event[MyEvent2]


# --- aggregate sample 2 ---


@dataclass(slots=True, frozen=True)
class YourId(Id):
    value: UUID

    @classmethod
    def new(self) -> YourId:
        return YourId(uuid7())


@dataclass(slots=True, frozen=True)
class YourEvent1:
    aggregate_id: YourId
    field1: str


type YourEvent = Event[YourEvent1]


# ----------------------------


def do_something(x: MyEvent | YourEvent) -> None:
    print(x.payload.aggregate_id)


def test_impl_example() -> None:
    my_id = MyId.new()
    your_id = YourId.new()

    e1 = Event(
        id_=EventId.new(),
        seq=1,
        occurred_at=datetime.now(),
        payload=MyEvent1(
            aggregate_id=my_id,
            value1="foo",
        ),
    )

    e2 = Event(
        id_=EventId.new(),
        seq=e1.next_seq(),
        occurred_at=datetime.now(),
        payload=MyEvent2(
            aggregate_id=my_id,
            value2="oo",
            value3="ee",
        ),
    )

    e3 = Event(
        id_=EventId.new(),
        seq=1,
        occurred_at=datetime.now(),
        payload=YourEvent1(
            aggregate_id=your_id,
            field1="bar",
        ),
    )

    do_something(e1)
    do_something(e2)
    do_something(e3)
