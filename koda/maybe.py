from dataclasses import dataclass
from typing import Any, Callable, Final, Generic, TypeVar, Union

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")

__all__ = (
    "Just",
    "Maybe",
    "Nothing",
    "NothingType",
)


@dataclass(frozen=True)
class NothingType:
    def map(self, _: Callable[[Any], Any]) -> "NothingType":
        """
        >>> Nothing.map(lambda _: 5)
        Nothing
        """
        return self

    def flat_map(self, _: Callable[[Any], Any]) -> "NothingType":
        return self

    def apply(self, _: "Maybe[Callable[[Any], Any]]") -> "NothingType":
        return self

    def __repr__(self) -> str:
        return "Nothing"


Nothing: Final[NothingType] = NothingType()


@dataclass(frozen=True)
class Just(Generic[A]):
    val: A

    def map(self, fn: Callable[[A], B]) -> "Just[B]":
        return Just(fn(self.val))

    def flat_map(self, fn: Callable[[A], "Maybe[B]"]) -> "Maybe[B]":
        return fn(self.val)

    def apply(self, container: "Maybe[Callable[[A], B]]") -> "Maybe[B]":
        if isinstance(container, NothingType):
            return Nothing
        else:
            return Just(container.val(self.val))


Maybe = Union[Just[A], NothingType]
