from dataclasses import dataclass

type Errors = InvalidValueErr | InvalidOperationErr


@dataclass(slots=True, frozen=True)
class InvalidValueErr:
    message: str


@dataclass(slots=True, frozen=True)
class InvalidOperationErr:
    message: str
