from typing import Callable, Optional, Tuple, Type, TypeVar, Union, overload

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


@overload
def _match(
    c1: Tuple[Type[A], Callable[[A], I]],
    c2: Tuple[Type[B], Callable[[B], I]],
) -> Callable[[Union[A, B]], I]:
    ...


@overload
def _match(
    c1: Tuple[Type[A], Callable[[A], I]],
    c2: Tuple[Type[B], Callable[[B], I]],
    c3: Tuple[Type[C], Callable[[C], I]],
) -> Callable[[Union[A, B, C]], I]:
    ...


@overload
def _match(
    c1: Tuple[Type[A], Callable[[A], I]],
    c2: Tuple[Type[B], Callable[[B], I]],
    c3: Tuple[Type[C], Callable[[C], I]],
    c4: Tuple[Type[D], Callable[[D], I]],
) -> Callable[[Union[A, B, C, D]], I]:
    ...


@overload
def _match(
    c1: Tuple[Type[A], Callable[[A], I]],
    c2: Tuple[Type[B], Callable[[B], I]],
    c3: Tuple[Type[C], Callable[[C], I]],
    c4: Tuple[Type[D], Callable[[D], I]],
    c5: Tuple[Type[E], Callable[[E], I]],
) -> Callable[[Union[A, B, C, D, E]], I]:
    ...


def _match(
    c1: Tuple[Type[A], Callable[[A], I]],
    c2: Tuple[Type[B], Callable[[B], I]],
    c3: Optional[Tuple[Type[C], Callable[[C], I]]] = None,
    c4: Optional[Tuple[Type[D], Callable[[D], I]]] = None,
    c5: Optional[Tuple[Type[E], Callable[[E], I]]] = None,
) -> Union[
    Callable[[Union[A, B]], I],
    Callable[[Union[A, B, C]], I],
    Callable[[Union[A, B, C, D]], I],
    Callable[[Union[A, B, C, D, E]], I],
]:
    if c3 is None:

        def inner2(val: Union[A, B]) -> I:
            if isinstance(val, c1[0]):
                assert isinstance(val, c1[0])
                return c1[1](val)
            else:
                assert isinstance(val, c2[0])
                return c2[1](val)

        return inner2
    elif c4 is None:

        def inner3(val: Union[A, B, C]) -> I:
            if isinstance(val, c1[0]):
                assert isinstance(val, c1[0])
                return c1[1](val)
            elif isinstance(val, c2[0]):
                assert isinstance(val, c2[0])
                return c2[1](val)
            else:
                assert isinstance(c3, tuple)
                assert isinstance(val, c3[0])
                return c3[1](val)

        return inner3
    elif c5 is None:

        def inner4(val: Union[A, B, C, D]) -> I:
            if isinstance(val, c1[0]):
                assert isinstance(val, c1[0])
                return c1[1](val)
            elif isinstance(val, c2[0]):
                assert isinstance(val, c2[0])
                return c2[1](val)
            else:
                assert isinstance(c3, tuple)
                if isinstance(val, c3[0]):
                    assert isinstance(val, c3[0])
                    return c3[1](val)
                else:
                    assert isinstance(c4, tuple)
                    assert isinstance(val, c4[0])
                    return c4[1](val)

        return inner4
    else:

        def inner5(val: Union[A, B, C, D, E]) -> I:
            if isinstance(val, c1[0]):
                assert isinstance(val, c1[0])
                return c1[1](val)
            elif isinstance(val, c2[0]):
                assert isinstance(val, c2[0])
                return c2[1](val)
            else:
                assert isinstance(c3, tuple)
                if isinstance(val, c3[0]):
                    assert isinstance(val, c3[0])
                    return c3[1](val)
                else:
                    assert c4 is not None
                    if isinstance(val, c4[0]):
                        assert isinstance(val, c4[0])
                        return c4[1](val)
                    else:
                        assert c5 is not None
                        assert isinstance(val, c5[0])
                        return c5[1](val)

        return inner5
