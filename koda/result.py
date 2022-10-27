from typing import TYPE_CHECKING, Any, Callable, Generic, Optional, Union

from koda._generics import A, B, FailT

if TYPE_CHECKING:  # pragma: no cover
    from koda.maybe import Maybe


class Ok(Generic[A]):
    __match_args__ = ("val",)
    __slots__ = ("val",)

    def __init__(self, val: A) -> None:
        self.val: A = val

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Ok) and other.val == self.val

    def __repr__(self) -> str:
        return f"Ok({self.val})"

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

    @property
    def to_optional(self) -> Optional[A]:
        """
        Note that `Ok[None]` will return None!
        """
        return self.val

    @property
    def to_maybe(self) -> "Maybe[A]":
        from koda.maybe import Just

        return Just(self.val)


class Err(Generic[FailT]):
    __match_args__ = ("val",)
    __slots__ = ("val",)

    def __init__(self, val: FailT) -> None:
        self.val: FailT = val

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Err) and other.val == self.val

    def __repr__(self) -> str:
        return f"Err({self.val})"

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

    @property
    def to_optional(self) -> Optional[Any]:
        return None

    @property
    def to_maybe(self) -> "Maybe[Any]":
        from koda.maybe import nothing

        return nothing


Result = Union[Ok[A], Err[FailT]]
