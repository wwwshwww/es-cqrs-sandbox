from dataclasses import dataclass

import uuid6


@dataclass(frozen=True)
class GroupId(uuid6.UUID):
    value: uuid6.UUID


def generate_group_id() -> GroupId:
    return GroupId(uuid6.uuid7())
