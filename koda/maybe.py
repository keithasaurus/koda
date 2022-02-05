from dataclasses import dataclass
from typing import Any, Callable, Final, Generic, Union

from koda._generics import A, B


@dataclass(frozen=True)
class Nothing:
    def map(self, _: Callable[[Any], Any]) -> "Nothing":
        """
        >>> nothing.map(lambda _: 5)
        Nothing
        """
        return self

    def flat_map(self, _: Callable[[Any], Any]) -> "Nothing":
        return self

    def apply(self, _: "Maybe[Callable[[Any], Any]]") -> "Nothing":
        return self

    def __repr__(self) -> str:
        return "Nothing"


# just a pre-init-ed instance of nothing.
nothing: Final[Nothing] = Nothing()


@dataclass(frozen=True)
class Just(Generic[A]):
    val: A

    def map(self, fn: Callable[[A], B]) -> "Just[B]":
        return Just(fn(self.val))

    def flat_map(self, fn: Callable[[A], "Maybe[B]"]) -> "Maybe[B]":
        return fn(self.val)

    def apply(self, container: "Maybe[Callable[[A], B]]") -> "Maybe[B]":
        if isinstance(container, Nothing):
            return nothing
        else:
            return Just(container.val(self.val))


Maybe = Union[Just[A], Nothing]
