from dataclasses import dataclass
from typing import Any, Callable, Generic, Union

from koda._generics import A, FailT, B


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
        """
        >>> def add_one(val: int) -> Result[int, Any]: return Err(val + 1)
        >>> Ok(5).flat_map_err(add_one)
        Ok(val=5)
        """
        return self

    def map(self, fn: Callable[[A], B]) -> "Ok[B]":
        return Ok(fn(self.val))

    def map_err(self, fn: Callable[[Any], Any]) -> "Ok[A]":
        return self

    def swap(self) -> "Err[A]":
        """
        >>> Ok(5).swap()
        Err(val=5)
        """
        return Err(self.val)


@dataclass(frozen=True)
class Err(Generic[FailT]):
    val: FailT

    def apply(self, _: "Result[Callable[[Any], Any], FailT]") -> "Err[FailT]":
        return self

    def map(self, _: Callable[[Any], Any]) -> "Err[FailT]":
        """
        >>> Err(3).map(lambda _: 25)
        Err(val=3)
        """
        return self

    def flat_map(self, _: Any) -> "Err[FailT]":
        return self

    def flat_map_err(
        self, fn: Callable[[FailT], "Result[A, FailT]"]
    ) -> "Result[A, FailT]":
        """
        >>> def add_one(val: int) -> Result[int, Any]: return Err(val + 1)
        >>> Err(5).flat_map_err(add_one)
        Err(val=6)
        """
        return fn(self.val)

    def map_err(self, fn: Callable[[FailT], B]) -> "Err[B]":
        """
        >>> def _int_to_str(n: int) -> str: return str(n)
        >>> Err(5).map_err(_int_to_str)
        Err(val='5')
        """
        return Err(fn(self.val))

    def swap(self) -> "Ok[FailT]":
        """
        >>> Err(3).swap()
        Ok(val=3)
        """
        return Ok(self.val)


Result = Union[Ok[A], Err[FailT]]
