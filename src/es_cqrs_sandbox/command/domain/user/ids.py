from dataclasses import dataclass

import uuid6


@dataclass(frozen=True)
class UserId(uuid6.UUID):
    value: uuid6.UUID


def generate_user_id() -> UserId:
    return UserId(uuid6.uuid7())
