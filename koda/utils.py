from typing import Any, Callable, List, Mapping, Optional, Protocol, TypeVar

from koda._cruft import _compose, _safe_try
from koda._generics import A, B, FailT
from koda.maybe import Just, Maybe, nothing
from koda.result import Err, Ok, Result

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


def to_maybe(val: Optional[A]) -> Maybe[A]:
    if val is None:
        return nothing
    else:
        return Just(val)


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


A_co = TypeVar("A_co", covariant=True)


class _AnyArgs(Protocol[A_co]):  # pragma: no cover
    def __call__(self, *args: Any, **kwargs: Any) -> A_co:
        ...


def always(x: A) -> _AnyArgs[A]:
    def inner(*args: Any, **kwargs: Any) -> A:
        return x

    return inner
