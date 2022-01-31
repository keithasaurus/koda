from typing import Any, Type

from koda.either import Fifth, First, Fourth, Second, Third
from tests.utils import enforce_functor_one_val


def _append_bla(s: str) -> str:
    return f"{s}bla"


def _test_first_returns_self(ordinal: Type[Any]) -> None:
    test_val = "a"
    assert ordinal(test_val).map_first(_append_bla) == ordinal(test_val)


def _test_second_returns_self(ordinal: Type[Any]) -> None:
    test_val = "a"
    assert ordinal(test_val).map_second(_append_bla) == ordinal(test_val)


def _test_third_returns_self(ordinal: Type[Any]) -> None:
    test_val = "a"
    assert ordinal(test_val).map_third(_append_bla) == ordinal(test_val)


def _test_fourth_returns_self(ordinal: Type[Any]) -> None:
    test_val = "a"
    assert ordinal(test_val).map_fourth(_append_bla) == ordinal(test_val)


def _test_fifth_returns_self(ordinal: Type[Any]) -> None:
    test_val = "a"
    assert ordinal(test_val).map_fifth(_append_bla) == ordinal(test_val)


def test_first() -> None:
    enforce_functor_one_val(First, "map_first")
    _test_second_returns_self(First)
    _test_third_returns_self(First)
    _test_fourth_returns_self(First)
    _test_fifth_returns_self(First)


def test_second() -> None:
    enforce_functor_one_val(Second, "map_second")
    _test_first_returns_self(Second)
    _test_third_returns_self(Second)
    _test_fourth_returns_self(Second)
    _test_fifth_returns_self(Second)


def test_third() -> None:
    enforce_functor_one_val(Third, "map_third")
    _test_first_returns_self(Third)
    _test_second_returns_self(Third)
    _test_fourth_returns_self(Third)
    _test_fifth_returns_self(Third)


def test_fourth() -> None:
    enforce_functor_one_val(Fourth, "map_fourth")
    _test_first_returns_self(Fourth)
    _test_second_returns_self(Fourth)
    _test_third_returns_self(Fourth)
    _test_fifth_returns_self(Fourth)


def test_fifth() -> None:
    enforce_functor_one_val(Fifth, "map_fifth")
    _test_first_returns_self(Fifth)
    _test_second_returns_self(Fifth)
    _test_third_returns_self(Fifth)
    _test_fourth_returns_self(Fifth)
