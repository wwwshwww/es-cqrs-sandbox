from dataclasses import dataclass
from typing import Protocol

from es_cqrs_sandbox.command.domain.common.event import Event, Metadata
from es_cqrs_sandbox.command.domain.group.ids import GroupId

from .ids import UserId
from .user import _Name


@dataclass(frozen=True)
class UserEvent(Event, Protocol):
    metadata: Metadata[UserId]


@dataclass(frozen=True)
class Created(UserEvent):
    metadata: Metadata[UserId]
    name: _Name
    belong_groups: list[GroupId]


@dataclass(frozen=True)
class Renamed(UserEvent):
    metadata: Metadata[UserId]
    name: _Name
