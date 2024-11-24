from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from es_cqrs_sandbox.command.domain.common.event import Metadata
from es_cqrs_sandbox.command.domain.group.ids import GroupId

from . import errors, events
from .ids import UserId


class Name(Protocol):
    @property
    def value(self) -> str: ...


@dataclass(frozen=True)
class _Name:
    value: str

    def validate_length(self) -> Result[None, errors.Error]:
        if (l := len(self.value)) == 0:
            return Failure(errors.InvalidValueError("Value cannot be empty"))
        elif l > 255:
            return Failure(errors.InvalidValueError("Value cannot be longer than 255 characters"))
        return Success(None)


def new_name(value: str) -> Result[Name, errors.Error]:
    n = _Name(value)
    rs = n.validate_length()

    if not is_successful(rs):
        return Failure(rs.failure())

    return Success(n)


def new_name_from(value: str) -> Name:
    return _Name(value)


class User(Protocol):
    @property
    def seq(self) -> int: ...
    @property
    def id_(self) -> UserId: ...
    @property
    def belong_groups(self) -> list[GroupId]: ...
    @property
    def name(self) -> Name: ...
    def validate(self) -> Result[None, errors.Error]: ...
    def rename(self, value: Name) -> Result[UserWithEventPair, errors.Error]: ...


type UserWithEventPair = tuple[User, events.UserEvent]


@dataclass(frozen=True)
class _User:
    seq: int
    id_: UserId
    belong_groups: list[GroupId]
    name: Name

    def validate(self) -> Result[None, errors.Error]:
        if len(self.belong_groups) == 0:
            return Failure(errors.InvalidValueError("Belong groups cannot be empty"))

        return Success(None)

    def rename(self, value: Name) -> Result[UserWithEventPair, errors.Error]:
        seq = self.seq + 1
        instance = new_user_from(
            seq,
            self.id_,
            self.belong_groups,
            value,
        )
        e = events.Renamed(
            metadata=Metadata(
                entity_id=self.id_,
                seq=seq,
            ),
            name=value,
        )
        return Success((instance, e))


def new_user(
    id_: UserId,
    belong_groups: list[GroupId],
    name: Name,
) -> Result[UserWithEventPair, errors.Error]:
    seq = 1
    instance = new_user_from(seq, id_, belong_groups, name)

    if not is_successful((rs := instance.validate())):
        return Failure(rs.failure())

    e = events.Created(
        metadata=Metadata(
            entity_id=id_,
            seq=seq,
        ),
        name=name,
        belong_groups=belong_groups,
    )
    return Success((instance, e))


def new_user_from(
    seq: int,
    id_: UserId,
    belong_groups: list[GroupId],
    name: Name,
) -> User:
    return _User(seq, id_, belong_groups, name)
