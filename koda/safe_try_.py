from typing import Callable, Final, Union, cast, overload

from koda._generics import A, B, C, D, E, F, G
from koda.result import Result, err, ok


class _Unset:
    pass


_unset: Final[_Unset] = _Unset()


@overload
def safe_try(fn: Callable[[A], B], v1: A) -> Result[B, Exception]:
    ...  # pragma: no cover


@overload
def safe_try(fn: Callable[[A, B], C], v1: A, v2: B) -> Result[C, Exception]:
    ...  # pragma: no cover


@overload
def safe_try(fn: Callable[[A, B, C], D], v1: A, v2: B, v3: C) -> Result[D, Exception]:
    ...  # pragma: no cover


@overload
def safe_try(
    fn: Callable[[A, B, C, D], E], v1: A, v2: B, v3: C, v4: D
) -> Result[E, Exception]:
    ...  # pragma: no cover


@overload
def safe_try(
    fn: Callable[[A, B, C, D, E], F], v1: A, v2: B, v3: C, v4: D, v5: E
) -> Result[F, Exception]:
    ...  # pragma: no cover


@overload
def safe_try(
    fn: Callable[[A, B, C, D, E, F], G], v1: A, v2: B, v3: C, v4: D, v5: E, v6: F
) -> Result[G, Exception]:
    ...  # pragma: no cover


def safe_try(
    fn: Union[
        Callable[[A], B],
        Callable[[A, B], C],
        Callable[[A, B, C], D],
        Callable[[A, B, C, D], E],
        Callable[[A, B, C, D, E], F],
        Callable[[A, B, C, D, E, F], G],
    ],
    v1: A,
    v2: Union[B, _Unset] = _unset,
    v3: Union[C, _Unset] = _unset,
    v4: Union[D, _Unset] = _unset,
    v5: Union[E, _Unset] = _unset,
    v6: Union[F, _Unset] = _unset,
) -> Union[
    Result[B, Exception],
    Result[C, Exception],
    Result[D, Exception],
    Result[E, Exception],
    Result[F, Exception],
    Result[G, Exception],
]:
    if isinstance(v2, _Unset):
        try:
            return ok(cast(Callable[[A], B], fn)(v1))
        except Exception as e:
            return err(e)
    elif isinstance(v3, _Unset):
        try:
            return ok(cast(Callable[[A, B], C], fn)(v1, v2))
        except Exception as e:
            return err(e)
    elif isinstance(v4, _Unset):
        try:
            return ok(cast(Callable[[A, B, C], D], fn)(v1, v2, v3))
        except Exception as e:
            return err(e)
    elif isinstance(v5, _Unset):
        try:
            return ok(cast(Callable[[A, B, C, D], E], fn)(v1, v2, v3, v4))
        except Exception as e:
            return err(e)
    elif isinstance(v6, _Unset):
        try:
            return ok(cast(Callable[[A, B, C, D, E], F], fn)(v1, v2, v3, v4, v5))
        except Exception as e:
            return err(e)
    else:
        try:
            return ok(cast(Callable[[A, B, C, D, E, F], G], fn)(v1, v2, v3, v4, v5, v6))
        except Exception as e:
            return err(e)
