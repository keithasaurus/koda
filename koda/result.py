from dataclasses import dataclass
from typing import Any, Callable, Generic, Union

from koda._generics import A, B, FailT


@dataclass(frozen=True)
class Ok(Generic[A]):
    val: A

    def apply(self, container: "Result[Callable[[A], B], FailT]") -> "Result[B, FailT]":
        if isinstance(container, Ok):
            return Ok(container.val(self.val))
        else:
            return container

    def get_or_else(self, _: A) -> A:
        return self.val

    def flat_map(self, fn: Callable[[A], "Result[B, FailT]"]) -> "Result[B, FailT]":
        return fn(self.val)

    def flat_map_err(self, fn: Callable[[Any], "Result[A, B]"]) -> "Result[A, B]":
        return self

    def map(self, fn: Callable[[A], B]) -> "Result[B, FailT]":
        return Ok(fn(self.val))

    def map_err(self, fn: Callable[[Any], "B"]) -> "Result[A, B]":
        return self

    def swap(self) -> "Result[FailT, A]":
        return Err(self.val)


@dataclass(frozen=True)
class Err(Generic[FailT]):
    val: FailT

    def apply(self, _: "Result[Callable[[Any], B], FailT]") -> "Result[B, FailT]":
        return self

    def get_or_else(self, fallback: A) -> A:
        return fallback

    def map(self, _: Callable[[Any], B]) -> "Result[B, FailT]":
        return self

    def flat_map(self, _: Callable[[Any], "Result[B, FailT]"]) -> "Result[B, FailT]":
        return self

    def flat_map_err(self, fn: Callable[[FailT], "Result[A, B]"]) -> "Result[A, B]":
        return fn(self.val)

    def map_err(self, fn: Callable[[FailT], B]) -> "Result[A, B]":
        return Err(fn(self.val))

    def swap(self) -> "Result[FailT, A]":
        return Ok(self.val)


Result = Union[Ok[A], Err[FailT]]
