from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar, Union

A = TypeVar("A")
B = TypeVar("B")

FailT = TypeVar("FailT")

__all__ = (
    'Failure',
    'Result',
    'Success',
)


@dataclass(frozen=True)
class Success(Generic[A]):
    val: A

    def apply(self,
              container: "Result[Callable[[A], B], FailT]") -> "Result[B, FailT]":
        if isinstance(container, Success):
            return Success(container.val(self.val))
        else:
            return container

    def flat_map(self,
                 fn: Callable[[A], "Result[B, FailT]"]) -> "Result[B, FailT]":
        return fn(self.val)

    def flat_map_failure(self,
                         fn: Callable[[Any], "Result[A, Any]"]) -> "Success[A]":
        """
        >>> def add_one(val: int) -> Result[int, Any]: return Failure(val + 1)
        >>> Success(5).flat_map_failure(add_one)
        Success(val=5)
        """
        return self

    def map(self, fn: Callable[[A], B]) -> "Success[B]":
        return Success(fn(self.val))

    def map_failure(self, fn: Callable[[Any], Any]) -> "Success[A]":
        return self

    def swap(self) -> "Failure[A]":
        """
        >>> Success(5).swap()
        Failure(val=5)
        """
        return Failure(self.val)


@dataclass(frozen=True)
class Failure(Generic[FailT]):
    val: FailT

    def apply(self, _: "Result[Callable[[Any], Any], FailT]") -> "Failure[FailT]":
        return self

    def map(self, _: Callable[[Any], Any]) -> "Failure[FailT]":
        """
        >>> Failure(3).map(lambda _: 25)
        Failure(val=3)
        """
        return self

    def flat_map(self, _: Any) -> "Failure[FailT]":
        return self

    def flat_map_failure(self,
                         fn: Callable[[FailT], "Result[A, FailT]"]) -> "Result[A, FailT]":
        """
        >>> def add_one(val: int) -> Result[int, Any]: return Failure(val + 1)
        >>> Failure(5).flat_map_failure(add_one)
        Failure(val=6)
        """
        return fn(self.val)

    def map_failure(self, fn: Callable[[FailT], B]) -> "Failure[B]":
        """
        >>> def _int_to_str(n: int) -> str: return str(n)
        >>> Failure(5).map_failure(_int_to_str)
        Failure(val='5')
        """
        return Failure(fn(self.val))

    def swap(self) -> "Success[FailT]":
        """
        >>> Failure(3).swap()
        Success(val=3)
        """
        return Success(self.val)


Result = Union[Success[A], Failure[FailT]]
