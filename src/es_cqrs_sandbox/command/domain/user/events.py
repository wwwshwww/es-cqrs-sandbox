from dataclasses import dataclass

from es_cqrs_sandbox.command.domain.common import event

from .ids import UserId

type UserEvent = UserRegistered | UserRenamed | UserEmailChanged


@dataclass(slots=True, frozen=True)
class UserRegistered(event.Event[UserId]):
    metadata: event.Metadata[UserId]

    name: str
    email: str
    email_version: int = 1


@dataclass(slots=True, frozen=True)
class UserRenamed(event.Event[UserId]):
    metadata: event.Metadata[UserId]

    old_name: str
    new_name: str


@dataclass(frozen=True)
class UserEmailChanged(event.Event[UserId]):
    metadata: event.Metadata[UserId]

    old_email: str
    new_email: str
