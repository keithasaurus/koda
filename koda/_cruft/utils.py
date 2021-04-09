from typing import Callable, Optional, TypeVar

from koda.result import Result

A = TypeVar("A")
FailT = TypeVar("FailT")


def _flat_map_same_type_if_not_none(fn: Optional[Callable[[A], Result[A, FailT]]],
                                    r: Result[A, FailT],
                                    ) -> Result[A, FailT]:
    if fn is None:
        return r
    else:
        return r.flat_map(fn)
