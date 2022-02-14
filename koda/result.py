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

    def flat_map(self, fn: Callable[[A], "Result[B, FailT]"]) -> "Result[B, FailT]":
        return fn(self.val)

    def flat_map_err(self, fn: Callable[[Any], "Result[A, Any]"]) -> "Ok[A]":
        return self

    def map(self, fn: Callable[[A], B]) -> "Ok[B]":
        return Ok(fn(self.val))

    def map_err(self, fn: Callable[[Any], "Any"]) -> "Ok[A]":
        return self

    def swap(self) -> "Err[A]":
        return Err(self.val)


@dataclass(frozen=True)
class Err(Generic[FailT]):
    val: FailT

    def apply(self, _: "Result[Callable[[Any], Any], FailT]") -> "Err[FailT]":
        return self

    def map(self, _: Callable[[Any], Any]) -> "Err[FailT]":
        return self

    def flat_map(self, _: Callable[[Any], "Result[Any, Any]"]) -> "Err[FailT]":
        return self

    def flat_map_err(self, fn: Callable[[FailT], "Result[A, B]"]) -> "Result[A, B]":
        return fn(self.val)

    def map_err(self, fn: Callable[[FailT], B]) -> "Err[B]":
        return Err(fn(self.val))

    def swap(self) -> Ok[FailT]:
        return Ok(self.val)


Result = Union[Ok[A], Err[FailT]]
