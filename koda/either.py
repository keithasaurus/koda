from dataclasses import dataclass
from typing import Any, Callable, Generic, Union

from koda._generics import A, B, C, D, E


@dataclass(frozen=True)
class First(Generic[A]):
    val: A

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


@dataclass(frozen=True)
class Second(Generic[A]):
    val: A

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


@dataclass(frozen=True)
class Third(Generic[A]):
    val: A

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


@dataclass(frozen=True)
class Fourth(Generic[A]):
    val: A

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


@dataclass(frozen=True)
class Fifth(Generic[A]):
    val: A

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
