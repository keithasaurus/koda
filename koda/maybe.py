from dataclasses import dataclass
from typing import Any, Callable, Final, Generic, Union

from koda import compose, identity
from koda._generics import A, B


@dataclass(frozen=True)
class Nothing:
    pass


@dataclass
class Just(Generic[A]):
    val: A


_Maybe = Nothing | Just[A]


@dataclass(frozen=True)
class Maybe(Generic[A]):
    val: _Maybe[A]

    def switch(self, if_just: Callable[[A], B], if_nothing: B) -> B:
        if isinstance(self.val, Just):
            return if_just(self.val.val)
        else:
            return if_nothing

    def get_or_else(self, fallback: A) -> A:
        return self.switch(identity, fallback)

    def map(self, fn: Callable[[A], B]) -> "Maybe[B]":
        return self.switch(compose(fn, just), nothing)

    def flat_map(self, fn: Callable[[A], "Maybe[B]"]) -> "Maybe[B]":
        return self.switch(fn, nothing)

    def apply(self, container: "Maybe[Callable[[A], B]]") -> "Maybe[B]":
        return container.switch(self.map, nothing)


nothing: Final[Maybe[Any]] = Maybe(Nothing())


def just(val: A) -> Maybe[A]:
    return Maybe(Just(val))
