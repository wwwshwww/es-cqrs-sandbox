from typing import Protocol


class AggregateRoot[T](Protocol):
    @property
    def identifier(self) -> T: ...

    def next_event_seq(self, num: int) -> list[int]: ...
