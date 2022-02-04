from typing import Any, Callable, Mapping, TypeVar, List

from koda._cruft.general import _compose, _safe_try
from koda.maybe import Just, Maybe, nothing
from koda.result import Err, Result, Ok

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")
G = TypeVar("G")
H = TypeVar("H")
I = TypeVar("I")

FailT = TypeVar("FailT")

__all__ = (
    "compose",
    "identity",
    "mapping_get",
    "load_once",
    "maybe_to_result",
    "result_to_maybe",
    "safe_try",
)

compose = _compose


def identity(x: A) -> A:
    return x


def mapping_get(data: Mapping[A, B], key: A) -> Maybe[B]:
    # this is better than data.get(...) because if None is a valid return value,
    # there's no way to know if the value is the value from the map or the deafult value
    try:
        return Just(data[key])
    except KeyError:
        return nothing


def maybe_to_result(fail_message: FailT, orig: Maybe[A]) -> Result[A, FailT]:
    if isinstance(orig, Just):
        return Ok(orig.val)
    else:
        return Err(fail_message)


def result_to_maybe(orig: Result[A, Any]) -> Maybe[A]:
    return Just(orig.val) if isinstance(orig, Ok) else nothing


def load_once(fn: Callable[[], A]) -> Callable[[], A]:
    """
    Lazily get some value
    """
    container: List[A] = []

    def inner() -> A:
        if len(container) == 0:
            val: A = fn()
            container.append(val)
            return val
        else:
            return container[0]

    return inner


safe_try = _safe_try
