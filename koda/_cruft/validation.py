from __future__ import annotations

from functools import partial
from typing import Callable, Optional, Tuple, TypeVar, Union, overload

from koda._cruft.utils import _flat_map_same_type_if_not_none
from koda.result import Failure, Result, Success

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")
G = TypeVar("G")
H = TypeVar("H")
I = TypeVar("I")
J = TypeVar("J")
K = TypeVar("K")

Ret = TypeVar("Ret")  # generic return type

FailT = TypeVar('FailT')

# simple alias allows to greatly reduce amount of characters required to define
# validators
_Validator = Callable[[A], Result[B, FailT]]


@overload
def _validate_and_map(
    r1: Result[A, FailT],
    r2: Callable[[A], Ret],
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    ...


@overload
def _validate_and_map(
    r1: Result[A, FailT],
    r2: Result[B, FailT],
    r3: Callable[[A, B], Ret],
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    ...


@overload
def _validate_and_map(
    r1: Result[A, FailT],
    r2: Result[B, FailT],
    r3: Result[C, FailT],
    r4: Callable[[A, B, C], Ret],
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    ...


@overload
def _validate_and_map(
    r1: Result[A, FailT],
    r2: Result[B, FailT],
    r3: Result[C, FailT],
    r4: Result[D, FailT],
    r5: Callable[[A, B, C, D], Ret],
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    ...


@overload
def _validate_and_map(r1: Result[A, FailT],
                      r2: Result[B, FailT],
                      r3: Result[C, FailT],
                      r4: Result[D, FailT],
                      r5: Result[E, FailT],
                      r6: Callable[[A, B, C, D, E], Ret],
                      *,
                      validate_object: Optional[
                          Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
                      ) -> Result[Ret, Tuple[FailT, ...]]:
    ...


@overload
def _validate_and_map(
    r1: Result[A, FailT],
    r2: Result[B, FailT],
    r3: Result[C, FailT],
    r4: Result[D, FailT],
    r5: Result[E, FailT],
    r6: Result[F, FailT],
    r7: Callable[[A, B, C, D, E, F], Ret],
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    ...


@overload
def _validate_and_map(
    r1: Result[A, FailT],
    r2: Result[B, FailT],
    r3: Result[C, FailT],
    r4: Result[D, FailT],
    r5: Result[E, FailT],
    r6: Result[F, FailT],
    r7: Result[G, FailT],
    r8: Callable[[A, B, C, D, E, F, G], Ret],
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    ...


@overload
def _validate_and_map(
    r1: Result[A, FailT],
    r2: Result[B, FailT],
    r3: Result[C, FailT],
    r4: Result[D, FailT],
    r5: Result[E, FailT],
    r6: Result[F, FailT],
    r7: Result[G, FailT],
    r8: Result[H, FailT],
    r9: Callable[[A, B, C, D, E, F, G, H], Ret],
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    ...


@overload
def _validate_and_map(
    r1: Result[A, FailT],
    r2: Result[B, FailT],
    r3: Result[C, FailT],
    r4: Result[D, FailT],
    r5: Result[E, FailT],
    r6: Result[F, FailT],
    r7: Result[G, FailT],
    r8: Result[H, FailT],
    r9: Result[I, FailT],
    r10: Callable[[A, B, C, D, E, F, G, H, I], Ret],
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    ...


@overload
def _validate_and_map(
    r1: Result[A, FailT],
    r2: Result[B, FailT],
    r3: Result[C, FailT],
    r4: Result[D, FailT],
    r5: Result[E, FailT],
    r6: Result[F, FailT],
    r7: Result[G, FailT],
    r8: Result[H, FailT],
    r9: Result[I, FailT],
    r10: Result[J, FailT],
    r11: Callable[[A, B, C, D, E, F, G, H, I, J], Ret],
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    ...


def _validate_and_map(
    r1: Result[A, FailT],
    r2: Callable[[A], Ret] | Result[B, FailT],
    r3: None | Callable[[A, B], Ret] | Result[C, FailT] = None,
    r4: None | Callable[[A, B, C], Ret] | Result[D, FailT] = None,
    r5: None | Callable[[A, B, C, D], Ret] | Result[E, FailT] = None,
    r6: None | Callable[[A, B, C, D, E], Ret] | Result[F, FailT] = None,
    r7: None | Callable[[A, B, C, D, E, F], Ret] | Result[G, FailT] = None,
    r8: None | Callable[[A, B, C, D, E, F, G], Ret] | Result[H, FailT] = None,
    r9: None | Callable[[A, B, C, D, E, F, G, H], Ret] | Result[I, FailT] = None,
    r10: None | Callable[[A, B, C, D, E, F, G, H, I], Ret] | Result[J, FailT] = None,
    r11: None | Callable[[A, B, C, D, E, F, G, H, I, J], Ret] = None,
    *,
    validate_object: Optional[Callable[[Ret], Result[Ret, Tuple[FailT, ...]]]] = None
) -> Result[Ret, Tuple[FailT, ...]]:
    """
    See overloaded signatures above for better idea of what's happening here

    Note that the assertions below should already be guaranteed by mypy
    """
    if callable(r2):
        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate1_helper(Success(r2), r1)
        )
    elif callable(r3):
        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate2_helper(Success(r3), r1, r2)
        )
    elif callable(r4):
        assert r3 is not None
        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate3_helper(Success(r4), r1, r2, r3)
        )
    elif callable(r5):
        assert r3 is not None
        assert r4 is not None
        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate4_helper(Success(r5), r1, r2, r3, r4)
        )
    elif callable(r6):
        assert r3 is not None
        assert r4 is not None
        assert r5 is not None

        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate5_helper(Success(r6), r1, r2, r3, r4, r5)
        )
    elif callable(r7):
        assert r3 is not None
        assert r4 is not None
        assert r5 is not None
        assert r6 is not None

        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate6_helper(Success(r7), r1, r2, r3, r4, r5, r6)
        )
    elif callable(r8):
        assert r3 is not None
        assert r4 is not None
        assert r5 is not None
        assert r6 is not None
        assert r7 is not None

        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate7_helper(Success(r8), r1, r2, r3, r4, r5, r6, r7)
        )
    elif callable(r9):
        assert r3 is not None
        assert r4 is not None
        assert r5 is not None
        assert r6 is not None
        assert r7 is not None
        assert r8 is not None

        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate8_helper(Success(r9), r1, r2, r3, r4, r5, r6, r7, r8)
        )
    elif callable(r10):
        assert r3 is not None
        assert r4 is not None
        assert r5 is not None
        assert r6 is not None
        assert r7 is not None
        assert r8 is not None
        assert r9 is not None

        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate9_helper(
                Success(r10),
                r1, r2, r3, r4, r5, r6, r7, r8, r9
            )
        )
    else:
        assert r3 is not None
        assert r4 is not None
        assert r5 is not None
        assert r6 is not None
        assert r7 is not None
        assert r8 is not None
        assert r9 is not None
        assert r10 is not None
        assert callable(r11)

        return _flat_map_same_type_if_not_none(
            validate_object,
            _validate10_helper(
                Success(r11),
                r1, r2, r3, r4, r5, r6, r7, r8, r9, r10
            )
        )


@overload
def _chain(fn1: _Validator[A, B, FailT],
           fn2: _Validator[B, C, FailT]
           ) -> _Validator[A, C, FailT]:
    ...


@overload
def _chain(fn1: _Validator[A, B, FailT],
           fn2: _Validator[B, C, FailT],
           fn3: _Validator[C, D, FailT]
           ) -> _Validator[A, D, FailT]:
    ...


@overload
def _chain(fn1: _Validator[A, B, FailT],
           fn2: _Validator[B, C, FailT],
           fn3: _Validator[C, D, FailT],
           fn4: _Validator[D, E, FailT]
           ) -> _Validator[A, E, FailT]:
    ...


@overload
def _chain(fn1: _Validator[A, B, FailT],
           fn2: _Validator[B, C, FailT],
           fn3: _Validator[C, D, FailT],
           fn4: _Validator[D, E, FailT],
           fn5: _Validator[E, F, FailT]
           ) -> _Validator[A, F, FailT]:
    ...


@overload
def _chain(fn1: _Validator[A, B, FailT],
           fn2: _Validator[B, C, FailT],
           fn3: _Validator[C, D, FailT],
           fn4: _Validator[D, E, FailT],
           fn5: _Validator[E, F, FailT],
           fn6: _Validator[F, G, FailT]
           ) -> _Validator[A, G, FailT]:
    ...


def _chain(fn1: _Validator[A, B, FailT],
           fn2: _Validator[B, C, FailT],
           fn3: Optional[_Validator[C, D, FailT]] = None,
           fn4: Optional[_Validator[D, E, FailT]] = None,
           fn5: Optional[_Validator[E, F, FailT]] = None,
           fn6: Optional[_Validator[F, G, FailT]] = None,
           ) -> Callable[[A], Union[Result[C, FailT],
                                    Result[D, FailT],
                                    Result[E, FailT],
                                    Result[F, FailT],
                                    Result[G, FailT]]]:
    def inner(val: A) -> Union[Result[C, FailT],
                               Result[D, FailT],
                               Result[E, FailT],
                               Result[F, FailT],
                               Result[G, FailT]]:
        if fn3 is None:
            return fn1(val).flat_map(fn2)
        elif fn4 is None:
            return fn1(val).flat_map(fn2).flat_map(fn3)
        elif fn5 is None:
            return fn1(val).flat_map(fn2).flat_map(fn3).flat_map(fn4)
        elif fn6 is None:
            return fn1(val).flat_map(fn2).flat_map(fn3).flat_map(fn4).flat_map(
                fn5)
        else:
            return fn1(val).flat_map(fn2).flat_map(fn3).flat_map(fn4).flat_map(
                fn5).flat_map(fn6)

    return inner


def _validate1_helper(
        state: Result[Callable[[A], B], Tuple[FailT, ...]],
        r: Result[A, FailT]
) -> Result[B, Tuple[FailT, ...]]:
    if isinstance(r, Failure):
        if isinstance(state, Failure):
            return Failure(state.val + (r.val,))
        else:
            return Failure((r.val,))
    else:
        if isinstance(state, Failure):
            return state
        else:
            return Success(state.val(r.val))


def _validate2_helper(
        state: Result[Callable[[A, B], C], Tuple[FailT, ...]],
        r1: Result[A, FailT],
        r2: Result[B, FailT],
) -> Result[C, Tuple[FailT, ...]]:
    if isinstance(r1, Failure):
        if isinstance(state, Failure):
            next_state: Result[Callable[[B], C], Tuple[FailT, ...]] = Failure(
                state.val + (r1.val,)
            )
        else:
            next_state = Failure((r1.val,))
    else:
        if isinstance(state, Failure):
            next_state = state
        else:
            next_state = Success(partial(state.val, r1.val))

    return _validate1_helper(next_state, r2)


def _validate3_helper(
        state: Result[Callable[[A, B, C], D], Tuple[FailT, ...]],
        r1: Result[A, FailT],
        r2: Result[B, FailT],
        r3: Result[C, FailT],
) -> Result[D, Tuple[FailT, ...]]:
    if isinstance(r1, Failure):
        if isinstance(state, Failure):
            next_state: Result[
                Callable[[B, C], D], Tuple[FailT, ...]] = Failure(
                state.val + (r1.val,)
            )
        else:
            next_state = Failure((r1.val,))
    else:
        if isinstance(state, Failure):
            next_state = state
        else:
            next_state = Success(partial(state.val, r1.val))

    return _validate2_helper(next_state, r2, r3)


def _validate4_helper(
        state: Result[Callable[[A, B, C, D], E], Tuple[FailT, ...]],
        r1: Result[A, FailT],
        r2: Result[B, FailT],
        r3: Result[C, FailT],
        r4: Result[D, FailT],
) -> Result[E, Tuple[FailT, ...]]:
    if isinstance(r1, Failure):
        if isinstance(state, Failure):
            next_state: Result[Callable[[B, C, D], E], Tuple[FailT, ...]] = \
                Failure(state.val + (r1.val,))
        else:
            next_state = Failure((r1.val,))
    else:
        if isinstance(state, Failure):
            next_state = state
        else:
            next_state = Success(partial(state.val, r1.val))

    return _validate3_helper(next_state, r2, r3, r4)


def _validate5_helper(
        state: Result[Callable[[A, B, C, D, E], F], Tuple[FailT, ...]],
        r1: Result[A, FailT],
        r2: Result[B, FailT],
        r3: Result[C, FailT],
        r4: Result[D, FailT],
        r5: Result[E, FailT],
) -> Result[F, Tuple[FailT, ...]]:
    if isinstance(r1, Failure):
        if isinstance(state, Failure):
            next_state: Result[
                Callable[[B, C, D, E], F],
                Tuple[FailT, ...]
            ] = Failure(state.val + (r1.val,))
        else:
            next_state = Failure((r1.val,))
    else:
        if isinstance(state, Failure):
            next_state = state
        else:
            next_state = Success(partial(state.val, r1.val))

    return _validate4_helper(next_state, r2, r3, r4, r5)


def _validate6_helper(
        state: Result[Callable[[A, B, C, D, E, F], G], Tuple[FailT, ...]],
        r1: Result[A, FailT],
        r2: Result[B, FailT],
        r3: Result[C, FailT],
        r4: Result[D, FailT],
        r5: Result[E, FailT],
        r6: Result[F, FailT],
) -> Result[G, Tuple[FailT, ...]]:
    if isinstance(r1, Failure):
        if isinstance(state, Failure):
            next_state: Result[
                Callable[[B, C, D, E, F], G],
                Tuple[FailT, ...]
            ] = Failure(state.val + (r1.val,))
        else:
            next_state = Failure((r1.val,))
    else:
        if isinstance(state, Failure):
            next_state = state
        else:
            next_state = Success(partial(state.val, r1.val))

    return _validate5_helper(next_state, r2, r3, r4, r5, r6)


def _validate7_helper(
        state: Result[
            Callable[[A, B, C, D, E, F, G], H], Tuple[FailT, ...]],
        r1: Result[A, FailT],
        r2: Result[B, FailT],
        r3: Result[C, FailT],
        r4: Result[D, FailT],
        r5: Result[E, FailT],
        r6: Result[F, FailT],
        r7: Result[G, FailT]
) -> Result[H, Tuple[FailT, ...]]:
    if isinstance(r1, Failure):
        if isinstance(state, Failure):
            next_state: Result[
                Callable[[B, C, D, E, F, G], H],
                Tuple[FailT, ...]
            ] = Failure(state.val + (r1.val,))
        else:
            next_state = Failure((r1.val,))
    else:
        if isinstance(state, Failure):
            next_state = state
        else:
            next_state = Success(partial(state.val, r1.val))

    return _validate6_helper(next_state, r2, r3, r4, r5, r6, r7)


def _validate8_helper(
        state: Result[
            Callable[[A, B, C, D, E, F, G, H], I],
            Tuple[FailT, ...]
        ],
        r1: Result[A, FailT],
        r2: Result[B, FailT],
        r3: Result[C, FailT],
        r4: Result[D, FailT],
        r5: Result[E, FailT],
        r6: Result[F, FailT],
        r7: Result[G, FailT],
        r8: Result[H, FailT]
) -> Result[I, Tuple[FailT, ...]]:
    if isinstance(r1, Failure):
        if isinstance(state, Failure):
            next_state: Result[
                Callable[[B, C, D, E, F, G, H], I],
                Tuple[FailT, ...]
            ] = Failure(state.val + (r1.val,))
        else:
            next_state = Failure((r1.val,))
    else:
        if isinstance(state, Failure):
            next_state = state
        else:
            next_state = Success(partial(state.val, r1.val))

    return _validate7_helper(next_state, r2, r3, r4, r5, r6, r7, r8)


def _validate9_helper(
        state: Result[
            Callable[[A, B, C, D, E, F, G, H, I], J],
            Tuple[FailT, ...]
        ],
        r1: Result[A, FailT],
        r2: Result[B, FailT],
        r3: Result[C, FailT],
        r4: Result[D, FailT],
        r5: Result[E, FailT],
        r6: Result[F, FailT],
        r7: Result[G, FailT],
        r8: Result[H, FailT],
        r9: Result[I, FailT]
) -> Result[J, Tuple[FailT, ...]]:
    if isinstance(r1, Failure):
        if isinstance(state, Failure):
            next_state: Result[
                Callable[[B, C, D, E, F, G, H, I], J],
                Tuple[FailT, ...]
            ] = Failure(state.val + (r1.val,))
        else:
            next_state = Failure((r1.val,))
    else:
        if isinstance(state, Failure):
            next_state = state
        else:
            next_state = Success(partial(state.val, r1.val))

    return _validate8_helper(next_state, r2, r3, r4, r5, r6, r7, r8, r9)


def _validate10_helper(
        state: Result[
            Callable[[A, B, C, D, E, F, G, H, I, J], K],
            Tuple[FailT, ...]
        ],
        r1: Result[A, FailT],
        r2: Result[B, FailT],
        r3: Result[C, FailT],
        r4: Result[D, FailT],
        r5: Result[E, FailT],
        r6: Result[F, FailT],
        r7: Result[G, FailT],
        r8: Result[H, FailT],
        r9: Result[I, FailT],
        r10: Result[J, FailT]
) -> Result[K, Tuple[FailT, ...]]:
    if isinstance(r1, Failure):
        if isinstance(state, Failure):
            next_state: Result[
                Callable[[B, C, D, E, F, G, H, I, J], K],
                Tuple[FailT, ...]
            ] = Failure(state.val + (r1.val,))
        else:
            next_state = Failure((r1.val,))
    else:
        if isinstance(state, Failure):
            next_state = state
        else:
            next_state = Success(partial(state.val, r1.val))

    return _validate9_helper(next_state, r2, r3, r4, r5, r6, r7, r8, r9, r10)
