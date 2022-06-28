from dataclasses import dataclass
from typing import Any, Callable, Generic, Union

from koda._generics import A, B, E, F
from koda.utils import always, compose, identity


@dataclass(frozen=True)
class Ok(Generic[A]):
    val: A


@dataclass(frozen=True)
class Err(Generic[E]):
    val: E


_Result = Ok[A] | Err[E]


@dataclass(frozen=True)
class Result(Generic[A, E]):
    val: _Result[A, E]

    def apply(self, container: "Result[Callable[[A], B], E]") -> "Result[B, E]":
        return container.switch(self.map, err)

    def if_ok(self, fn: Callable[[A], Any]) -> None:
        self.switch(fn, lambda _: None)

    def if_err(self, fn: Callable[[E], Any]) -> None:
        self.switch(lambda _: None, fn)

    def get_or_else(self, fallback: A) -> A:
        return self.switch(
            # not sure why, but identity not passing type checks here
            lambda x: x,
            always(fallback),
        )

    def get_err_or_else(self, fallback: E) -> E:
        return self.switch(always(fallback), lambda a: a)

    def map(self, fn: Callable[[A], B]) -> "Result[B, E]":
        return self.switch(compose(fn, ok), err)

    def map_err(self, fn: Callable[[E], F]) -> "Result[A, F]":
        return self.switch(ok, compose(fn, err))

    def flat_map(self, fn: Callable[[A], "Result[B, E]"]) -> "Result[B, E]":
        return self.switch(fn, err)

    def flat_map_err(self, fn: Callable[[E], "Result[A, F]"]) -> "Result[A, F]":
        return self.switch(ok, fn)

    def swap(self) -> "Result[E, A]":
        return self.switch(err, ok)

    def switch(self, if_ok: Callable[[A], B], if_err: Callable[[E], B]) -> B:
        if isinstance(self.val, Ok):
            return if_ok(self.val.val)
        else:
            return if_err(self.val.val)


def ok(val: A) -> Result[A, Any]:
    return Result(Ok(val))


def err(val: E) -> Result[Any, E]:
    return Result(Err(val))
