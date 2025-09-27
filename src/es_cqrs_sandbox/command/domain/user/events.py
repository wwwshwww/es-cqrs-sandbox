from dataclasses import dataclass

from es_cqrs_sandbox.command.domain.common.types import Event

from .ids import UserId


@dataclass(slots=True, frozen=True)
class UserRegistered:
    aggregate_id: UserId

    name: str
    email: str
    email_version: int


@dataclass(slots=True, frozen=True)
class UserRenamed:
    aggregate_id: UserId

    old_name: str
    new_name: str


@dataclass(frozen=True)
class UserEmailChanged:
    aggregate_id: UserId

    email_version: int
    old_email: str
    new_email: str


type UserEvent = Event[UserRegistered] | Event[UserRenamed] | Event[UserEmailChanged]
