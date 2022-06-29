from dataclasses import dataclass
from typing import Any, Callable, Final, Generic, Union

from koda._generics import A, B


@dataclass(frozen=True)
class Nothing:
    def get_or_else(self, fallback: A) -> A:
        return fallback

    def map(self, _: Callable[[Any], B]) -> "Maybe[B]":
        return self

    def flat_map(self, _: Callable[[Any], "Maybe[B]"]) -> "Maybe[B]":
        return self

    def apply(self, _: "Maybe[Callable[[Any], B]]") -> "Maybe[B]":
        return self


# just a pre-init-ed instance of nothing.
nothing: Final[Nothing] = Nothing()


@dataclass(frozen=True)
class Just(Generic[A]):
    val: A

    def get_or_else(self, _: Any) -> A:
        return self.val

    def map(self, fn: Callable[[A], B]) -> "Maybe[B]":
        return Just(fn(self.val))

    def flat_map(self, fn: Callable[[A], "Maybe[B]"]) -> "Maybe[B]":
        return fn(self.val)

    def apply(self, container: "Maybe[Callable[[A], B]]") -> "Maybe[B]":
        if isinstance(container, Nothing):
            return nothing
        else:
            return Just(container.val(self.val))


Maybe = Union[Just[A], Nothing]
