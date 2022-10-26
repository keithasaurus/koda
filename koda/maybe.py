from dataclasses import dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Final,
    Generic,
    Optional,
    Union,
)

from koda._generics import A, B, FailT

if TYPE_CHECKING:  # pragma: no cover
    from koda.result import Result


class Nothing:
    _instance: ClassVar[Optional["Nothing"]] = None

    def __new__(cls) -> "Nothing":
        """
        Make `Nothing` a singleton, so we can do `is` checks if we want.
        """
        if cls._instance is None:
            cls._instance = super(Nothing, cls).__new__(cls)
        return cls._instance

    def get_or_else(self, fallback: A) -> A:
        return fallback

    def map(self, _: Callable[[Any], B]) -> "Maybe[B]":
        return self

    def flat_map(self, _: Callable[[Any], "Maybe[B]"]) -> "Maybe[B]":
        return self

    def apply(self, _: "Maybe[Callable[[Any], B]]") -> "Maybe[B]":
        return self

    @property
    def to_optional(self) -> Optional[Any]:
        """
        Note that `Just[None]` will return None!
        """
        return None

    def to_result(self, fail_obj: FailT) -> "Result[Any, FailT]":
        from koda.result import Err

        return Err(fail_obj)


# just a pre-init-ed instance of nothing.
nothing: Final[Nothing] = Nothing()


@dataclass
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

    @property
    def to_optional(self) -> Optional[A]:
        return self.val

    def to_result(self, fail_obj: FailT) -> "Result[A, FailT]":
        from koda.result import Ok

        return Ok(self.val)


Maybe = Union[Just[A], Nothing]
