from dataclasses import dataclass

from src.es_cqrs_sandbox.command.domain.common import types

from .ids import UserId

type UserEvent = UserRegistered | UserRenamed | UserEmailChanged


@dataclass(slots=True, frozen=True)
class UserRegistered:
    metadata: types.EventMetadata[UserId]

    name: str
    email: str
    email_version: int = 1


@dataclass(slots=True, frozen=True)
class UserRenamed:
    metadata: types.EventMetadata[UserId]

    old_name: str
    new_name: str


@dataclass(frozen=True)
class UserEmailChanged:
    metadata: types.EventMetadata[UserId]

    old_email: str
    new_email: str
