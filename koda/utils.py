from typing import Any, Callable, List, Protocol, TypeVar

from koda._generics import A


def identity(x: A) -> A:
    return x


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


A_co = TypeVar("A_co", covariant=True)


class _AnyArgs(Protocol[A_co]):  # pragma: no cover
    def __call__(self, *args: Any, **kwargs: Any) -> A_co:
        ...


def always(x: A) -> _AnyArgs[A]:
    def inner(*args: Any, **kwargs: Any) -> A:
        return x

    return inner
