from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from returns.pipeline import is_successful
from returns.result import Failure, Result, ResultE, Success, safe

from es_cqrs_sandbox.command.domain.common.entity import AggregateRoot
from es_cqrs_sandbox.command.domain.common.event import Metadata
from es_cqrs_sandbox.command.domain.group.ids import GroupId

from . import errors, events
from .ids import UserId


@dataclass(frozen=True)
class _Name:
    value: str

    def __post_init__(self):
        if (l := len(self.value)) == 0:
            raise ValueError("Value cannot be empty")
        elif l > 255:
            raise ValueError("Value cannot be longer than 255 characters")


def new_name(value: str) -> ResultE[_Name]:
    return safe(_Name)(value)


class _User(AggregateRoot[UserId]):
    def __init__(
        self,
        _seq_manager: Callable[[int], list[int]],
        identifier: UserId,
        belong_groups: list[GroupId],
        name: _Name,
    ) -> None:
        self._seq_manager = _seq_manager

        self._identifier = identifier
        self._belong_groups = belong_groups
        self._name = name

    @property
    def identifier(self) -> UserId:
        return self._identifier

    def next_event_seq(self, num: int) -> list[int]:
        return self._seq_manager(num)

    @property
    def belong_groups(self) -> list[GroupId]:
        return self._belong_groups

    @property
    def name(self) -> _Name:
        return self._name

    def rename(self, value: _Name) -> Result[events.Renamed, errors.Error]:
        self._name = value

        event_seq = self.next_event_seq(1)[0]

        return Success(
            events.Renamed(
                metadata=Metadata(
                    entity_id=self._identifier,
                    seq=event_seq,
                    timestamp=datetime.now(),
                ),
                name=self._name,
            )
        )


def new_user(
    seq_manager: Callable[[int], list[int]],
    identifier: UserId,
    belong_groups: list[GroupId],
    name: _Name,
) -> Result[_User, errors.Error]:
    rs = safe(_User)(seq_manager, identifier, belong_groups, name)

    if is_successful(rs):
        return Success(rs.unwrap())
    else:
        return Failure(errors.InvalidOperationError(str(rs.failure())))
