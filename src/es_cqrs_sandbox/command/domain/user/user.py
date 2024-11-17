from __future__ import annotations

from dataclasses import dataclass

from returns.pipeline import is_successful
from returns.result import Failure, Result, Success

from es_cqrs_sandbox.command.domain.common.event import Metadata
from es_cqrs_sandbox.command.domain.group.ids import GroupId

from . import errors, events
from .ids import UserId

type UserWithEventPair = tuple[_User, events.UserEvent]


@dataclass(frozen=True)
class _Name:
    value: str

    def validate_length(self) -> Result[None, errors.Error]:
        if (l := len(self.value)) == 0:
            return Failure(errors.InvalidValueError("Value cannot be empty"))
        elif l > 255:
            return Failure(
                errors.InvalidValueError("Value cannot be longer than 255 characters")
            )
        return Success(None)


def new_name(value: str) -> Result[_Name, errors.Error]:
    n = _Name(value)
    rs = n.validate_length()

    if not is_successful(rs):
        return Failure(rs.failure())

    return Success(n)


def new_name_from(value: str) -> _Name:
    return _Name(value)


@dataclass(frozen=True)
class _User:
    seq: int
    identifier: UserId
    belong_groups: list[GroupId]
    name: _Name

    def validate(self) -> Result[None, errors.Error]:
        if len(self.belong_groups) == 0:
            return Failure(errors.InvalidValueError("Belong groups cannot be empty"))

        return Success(None)

    def rename(self, value: _Name) -> Result[UserWithEventPair, errors.Error]:
        seq = self.seq + 1
        instance = new_user_from(
            seq,
            self.identifier,
            self.belong_groups,
            value,
        )
        e = events.Renamed(
            metadata=Metadata(
                entity_id=self.identifier,
                seq=seq,
            ),
            name=value,
        )
        return Success((instance, e))


def new_user(
    identifier: UserId,
    belong_groups: list[GroupId],
    name: _Name,
) -> Result[UserWithEventPair, errors.Error]:
    seq = 1
    instance = new_user_from(seq, identifier, belong_groups, name)

    if not is_successful((rs := instance.validate())):
        return Failure(rs.failure())

    e = events.Created(
        metadata=Metadata(
            entity_id=identifier,
            seq=seq,
        ),
        name=name,
        belong_groups=belong_groups,
    )
    return Success((instance, e))


def new_user_from(
    seq: int,
    identifier: UserId,
    belong_groups: list[GroupId],
    name: _Name,
) -> _User:
    return _User(seq, identifier, belong_groups, name)
