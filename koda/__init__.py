from typing import Any, Callable, List, Mapping, TypeVar

from koda._cruft.general import _compose, _match
from koda.maybe import Just, Maybe, Nothing
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
    'compose',
    'get_mapping_val',
    'identity',
    'match',
    'load_once',
    'maybe_to_result',
    'result_to_maybe',
)

compose = _compose

match = _match


def identity(x: A) -> A:
    return x


def get_mapping_val(key: A) -> Callable[[Mapping[A, B]], Maybe[B]]:
    def inner(data: Mapping[A, B], ) -> Maybe[B]:
        # this is better than data.get(...) because None could be a valid vale
        try:
            return Just(data[key])
        except KeyError:
            return Nothing

    return inner


def maybe_to_result(
        fail_message: FailT
) -> Callable[[Maybe[A]], Result[A, FailT]]:
    def inner(orig: Maybe[A]) -> Result[A, FailT]:
        if isinstance(orig, Just):
            return Ok(orig.val)
        else:
            return Err(fail_message)

    return inner


def result_to_maybe(orig: Result[A, Any]) -> Maybe[A]:
    if isinstance(orig, Ok):
        return Just(orig.val)
    else:
        return Nothing


def thunkify(obj: A) -> Callable[[], A]:
    def inner() -> A:
        return obj

    return inner


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


def safe_try(fn: Callable[[A], B]) -> Callable[[A], Result[B, Exception]]:
    def inner(val: A) -> Result[B, Exception]:
        try:
            return Ok(fn(val))
        except Exception as e:
            return Err(e)
    return inner
