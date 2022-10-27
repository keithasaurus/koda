from typing import Any, Callable, Generic, Union

from koda._generics import A, B, C, D, E


class First(Generic[A]):
    __slots__ = ("val",)
    __match_args__ = ("val",)

    def __init__(self, val: A) -> None:
        self.val: A = val

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, First) and other.val == self.val

    def __repr__(self) -> str:
        return f"First({self.val})"

    def map_first(self, fn: Callable[[A], B]) -> "First[B]":
        return First(fn(self.val))

    def map_second(self, fn: Callable[[Any], Any]) -> "First[A]":
        return self

    def map_third(self, fn: Callable[[Any], Any]) -> "First[A]":
        return self

    def map_fourth(self, fn: Callable[[Any], Any]) -> "First[A]":
        return self

    def map_fifth(self, fn: Callable[[Any], Any]) -> "First[A]":
        return self


class Second(Generic[A]):
    __slots__ = ("val",)
    __match_args__ = ("val",)

    def __init__(self, val: A) -> None:
        self.val: A = val

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Second) and other.val == self.val

    def __repr__(self) -> str:
        return f"Second({self.val})"

    def map_first(self, fn: Callable[[Any], Any]) -> "Second[A]":
        return self

    def map_second(self, fn: Callable[[A], B]) -> "Second[B]":
        return Second(fn(self.val))

    def map_third(self, fn: Callable[[Any], Any]) -> "Second[A]":
        return self

    def map_fourth(self, fn: Callable[[Any], Any]) -> "Second[A]":
        return self

    def map_fifth(self, fn: Callable[[Any], Any]) -> "Second[A]":
        return self


class Third(Generic[A]):
    __slots__ = ("val",)
    __match_args__ = ("val",)

    def __init__(self, val: A) -> None:
        self.val: A = val

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Third) and other.val == self.val

    def __repr__(self) -> str:
        return f"Third({self.val})"

    def map_first(self, fn: Callable[[Any], Any]) -> "Third[A]":
        return self

    def map_second(self, fn: Callable[[Any], Any]) -> "Third[A]":
        return self

    def map_third(self, fn: Callable[[A], B]) -> "Third[B]":
        return Third(fn(self.val))

    def map_fourth(self, fn: Callable[[Any], Any]) -> "Third[A]":
        return self

    def map_fifth(self, fn: Callable[[Any], Any]) -> "Third[A]":
        return self


class Fourth(Generic[A]):
    __slots__ = ("val",)
    __match_args__ = ("val",)

    def __init__(self, val: A) -> None:
        self.val: A = val

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Fourth) and other.val == self.val

    def __repr__(self) -> str:
        return f"Fourth({self.val})"

    def map_first(self, fn: Callable[[Any], Any]) -> "Fourth[A]":
        return self

    def map_second(self, fn: Callable[[Any], Any]) -> "Fourth[A]":
        return self

    def map_third(self, fn: Callable[[Any], Any]) -> "Fourth[A]":
        return self

    def map_fourth(self, fn: Callable[[A], B]) -> "Fourth[B]":
        return Fourth(fn(self.val))

    def map_fifth(self, fn: Callable[[Any], Any]) -> "Fourth[A]":
        return self


class Fifth(Generic[A]):
    __slots__ = ("val",)
    __match_args__ = ("val",)

    def __init__(self, val: A) -> None:
        self.val: A = val

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Fifth) and other.val == self.val

    def __repr__(self) -> str:
        return f"Fifth({self.val})"

    def map_first(self, fn: Callable[[Any], Any]) -> "Fifth[A]":
        return self

    def map_second(self, fn: Callable[[Any], Any]) -> "Fifth[A]":
        return self

    def map_third(self, fn: Callable[[Any], Any]) -> "Fifth[A]":
        return self

    def map_fourth(self, fn: Callable[[Any], Any]) -> "Fifth[A]":
        return self

    def map_fifth(self, fn: Callable[[A], B]) -> "Fifth[B]":
        return Fifth(fn(self.val))


Either = Union[First[A], Second[B]]
Either3 = Union[First[A], Second[B], Third[C]]
Either4 = Union[First[A], Second[B], Third[C], Fourth[D]]
Either5 = Union[First[A], Second[B], Third[C], Fourth[D], Fifth[E]]
