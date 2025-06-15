from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Self

from returns import result
from returns.pipeline import is_successful
from uuid6 import uuid7

from es_cqrs_sandbox.command.domain.common import event
from es_cqrs_sandbox.command.domain.group.ids import GroupId

from .errors import Errors, InvalidOperationErr, InvalidValueErr
from .events import UserEvent, UserRegistered, UserRenamed
from .ids import UserId

type UserWithEventPair = tuple[User, UserEvent]


@dataclass(slots=True, frozen=True)
class User:
    seq: int

    id_: UserId
    belong_groups: list[GroupId]
    name: str
    email: Email

    def validate(self) -> result.Result[Self, Errors]:
        if len(self.belong_groups) < 0:
            return result.Failure(InvalidValueErr("Belong groups must be at least 0."))
        if len(self.belong_groups) > 10:
            return result.Failure(InvalidValueErr("Belong groups must be at most 10."))

        return result.Success(self)

    @classmethod
    def new(
        cls, belong_groups: list[GroupId], name: str, email: Email, timestamp: datetime
    ) -> result.Result[UserWithEventPair, Errors]:
        seq = 0
        id_ = UserId(uuid7())
        return (
            cls(seq=seq, id_=id_, belong_groups=belong_groups, name=name, email=email)
            .validate()
            .map(
                lambda valid_user: (
                    valid_user,
                    UserRegistered(
                        metadata=event.Metadata(aggregate_id=valid_user.id_, seq=seq, occurred_at=timestamp),
                        name=valid_user.name,
                        email=valid_user.email.value,
                    ),
                )
            )
        )

    def rename(self, new_name: str, timestamp: datetime) -> result.Result[UserWithEventPair, Errors]:
        seq = self.seq + 1
        return (
            self.__class__(
                seq=seq,
                id_=self.id_,
                belong_groups=self.belong_groups,
                name=new_name,
                email=self.email,
            )
            .validate()
            .map(
                lambda valid_user: (
                    valid_user,
                    UserRenamed(
                        metadata=event.Metadata(aggregate_id=valid_user.id_, seq=seq, occurred_at=timestamp),
                        old_name=self.name,
                        new_name=valid_user.name,
                    ),
                )
            )
        )


@dataclass(slots=True, frozen=True)
class Email:
    value: str

    @classmethod
    def new(cls, value: str) -> result.Result[Self, Exception]:
        if (len(value) < 0) or (len(value) > 256):
            return result.Failure(ValueError("Email length must be between 1 and 256 characters."))
        if not all(x in value for x in {"@", "."}):
            return result.Failure(ValueError("Email must contain '@' and '.' characters."))

        return result.Success(cls(value))
