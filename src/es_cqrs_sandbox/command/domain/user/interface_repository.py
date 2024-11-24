from dataclasses import dataclass
from typing import Protocol

from returns.result import ResultE

from .events import UserEvent
from .ids import UserId
from .user import User


@dataclass(frozen=True)
class SaveDto:
    entity: User
    events: list[UserEvent]


class Repository(Protocol):
    def bulk_save(self, targets: list[SaveDto]) -> ResultE[None]:
        """イベントストア & スナップショットストアへに対してデータ永続化を実施する"""
        ...

    def bulk_get(self, ids: list[UserId]) -> dict[UserId, User]:
        """スナップショットストアからデータを取得する"""
        ...

    # def find(self, fo: FilteringOptions, so: list[SortingOption]) -> list[UserId]:
    #     """スナップショットストアを検索し、条件ヒットするエンティティの識別子を指定順序で返却する"""
    #     ...
