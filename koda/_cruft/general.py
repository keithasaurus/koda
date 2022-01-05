from typing import Callable, Optional, TypeVar, Union, overload

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


@overload
def _compose(fn1: Callable[[A], B], fn2: Callable[[B], C]) -> Callable[[A], C]:
    ...


@overload
def _compose(
    fn1: Callable[[A], B], fn2: Callable[[B], C], fn3: Callable[[C], D]
) -> Callable[[A], D]:
    ...


@overload
def _compose(
    fn1: Callable[[A], B],
    fn2: Callable[[B], C],
    fn3: Callable[[C], D],
    fn4: Callable[[D], E],
) -> Callable[[A], E]:
    ...


@overload
def _compose(
    fn1: Callable[[A], B],
    fn2: Callable[[B], C],
    fn3: Callable[[C], D],
    fn4: Callable[[D], E],
    fn5: Callable[[E], F],
) -> Callable[[A], F]:
    ...


@overload
def _compose(
    fn1: Callable[[A], B],
    fn2: Callable[[B], C],
    fn3: Callable[[C], D],
    fn4: Callable[[D], E],
    fn5: Callable[[E], F],
    fn6: Callable[[F], G],
) -> Callable[[A], G]:
    ...


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
    ...


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
    ...


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
