from typing import Callable, Final, Optional, Union, cast, overload

from koda._generics import A, B, C, D, E, F, G, H, I
from koda.result import Err, Ok, Result


@overload
def _compose(fn1: Callable[[A], B], fn2: Callable[[B], C]) -> Callable[[A], C]:
    ...  # pragma: no cover


@overload
def _compose(
    fn1: Callable[[A], B], fn2: Callable[[B], C], fn3: Callable[[C], D]
) -> Callable[[A], D]:
    ...  # pragma: no cover


@overload
def _compose(
    fn1: Callable[[A], B],
    fn2: Callable[[B], C],
    fn3: Callable[[C], D],
    fn4: Callable[[D], E],
) -> Callable[[A], E]:
    ...  # pragma: no cover


@overload
def _compose(
    fn1: Callable[[A], B],
    fn2: Callable[[B], C],
    fn3: Callable[[C], D],
    fn4: Callable[[D], E],
    fn5: Callable[[E], F],
) -> Callable[[A], F]:
    ...  # pragma: no cover


@overload
def _compose(
    fn1: Callable[[A], B],
    fn2: Callable[[B], C],
    fn3: Callable[[C], D],
    fn4: Callable[[D], E],
    fn5: Callable[[E], F],
    fn6: Callable[[F], G],
) -> Callable[[A], G]:
    ...  # pragma: no cover


@overload
def _compose(
    fn1: Callable[[A], B],
    fn2: Callable[[B], C],
    fn3: Callable[[C], D],
    fn4: Callable[[D], E],
    fn5: Callable[[E], F],
    fn6: Callable[[F], G],
    fn7: Callable[[G], H],
) -> Callable[[A], H]:
    ...  # pragma: no cover


@overload
def _compose(
    fn1: Callable[[A], B],
    fn2: Callable[[B], C],
    fn3: Callable[[C], D],
    fn4: Callable[[D], E],
    fn5: Callable[[E], F],
    fn6: Callable[[F], G],
    fn7: Callable[[G], H],
    fn8: Callable[[H], I],
) -> Callable[[A], I]:
    ...  # pragma: no cover


def _compose(
    fn1: Callable[[A], B],
    fn2: Callable[[B], C],
    fn3: Optional[Callable[[C], D]] = None,
    fn4: Optional[Callable[[D], E]] = None,
    fn5: Optional[Callable[[E], F]] = None,
    fn6: Optional[Callable[[F], G]] = None,
    fn7: Optional[Callable[[G], H]] = None,
    fn8: Optional[Callable[[H], I]] = None,
) -> Callable[[A], Union[C, D, E, F, G, H, I]]:
    def inner(obj: A) -> Union[C, D, E, F, G, H, I]:
        if fn3 is None:
            return fn2(fn1(obj))
        elif fn4 is None:
            return fn3(fn2(fn1(obj)))
        elif fn5 is None:
            return fn4(fn3(fn2(fn1(obj))))
        elif fn6 is None:
            return fn5(fn4(fn3(fn2(fn1(obj)))))
        elif fn7 is None:
            return fn6(fn5(fn4(fn3(fn2(fn1(obj))))))
        elif fn8 is None:
            return fn7(fn6(fn5(fn4(fn3(fn2(fn1(obj)))))))
        else:
            return fn8(fn7(fn6(fn5(fn4(fn3(fn2(fn1(obj))))))))

    return inner


class _Unset:
    pass


_unset: Final[_Unset] = _Unset()


@overload
def _safe_try(fn: Callable[[A], B], v1: A) -> Result[B, Exception]:
    ...  # pragma: no cover


@overload
def _safe_try(fn: Callable[[A, B], C], v1: A, v2: B) -> Result[C, Exception]:
    ...  # pragma: no cover


@overload
def _safe_try(fn: Callable[[A, B, C], D], v1: A, v2: B, v3: C) -> Result[D, Exception]:
    ...  # pragma: no cover


@overload
def _safe_try(
    fn: Callable[[A, B, C, D], E], v1: A, v2: B, v3: C, v4: D
) -> Result[E, Exception]:
    ...  # pragma: no cover


@overload
def _safe_try(
    fn: Callable[[A, B, C, D, E], F], v1: A, v2: B, v3: C, v4: D, v5: E
) -> Result[F, Exception]:
    ...  # pragma: no cover


@overload
def _safe_try(
    fn: Callable[[A, B, C, D, E, F], G], v1: A, v2: B, v3: C, v4: D, v5: E, v6: F
) -> Result[G, Exception]:
    ...  # pragma: no cover


def _safe_try(
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
            return Ok(cast(Callable[[A], B], fn)(v1))
        except Exception as e:
            return Err(e)
    elif isinstance(v3, _Unset):
        try:
            return Ok(cast(Callable[[A, B], C], fn)(v1, v2))
        except Exception as e:
            return Err(e)
    elif isinstance(v4, _Unset):
        try:
            return Ok(cast(Callable[[A, B, C], D], fn)(v1, v2, v3))
        except Exception as e:
            return Err(e)
    elif isinstance(v5, _Unset):
        try:
            return Ok(cast(Callable[[A, B, C, D], E], fn)(v1, v2, v3, v4))
        except Exception as e:
            return Err(e)
    elif isinstance(v6, _Unset):
        try:
            return Ok(cast(Callable[[A, B, C, D, E], F], fn)(v1, v2, v3, v4, v5))
        except Exception as e:
            return Err(e)
    else:
        try:
            return Ok(cast(Callable[[A, B, C, D, E, F], G], fn)(v1, v2, v3, v4, v5, v6))
        except Exception as e:
            return Err(e)
