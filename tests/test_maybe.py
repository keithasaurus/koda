from typing import Any

from koda.maybe import just, nothing
from tests.utils import (
    enforce_applicative_apply,
    enforce_functor_one_val,
    enforce_monad_flat_map,
    enforce_monad_unit,
)


def test_maybe() -> None:
    enforce_functor_one_val(just, "map")
    enforce_monad_unit(just)
    enforce_monad_flat_map(just, nothing)
    enforce_applicative_apply(just, nothing)


def test_nothing_map() -> None:
    def anything_to_5(_: Any) -> int:
        return 5

    assert nothing.map(anything_to_5) == nothing


def test_get_or_else() -> None:
    assert just(5).get_or_else(12) == 5
    assert nothing.get_or_else(12) == 12


def test_if_just() -> None:
    box: list[int] = []

    nothing.if_just(box.append)
    assert box == []

    just(10).if_just(box.append)
    assert box == [10]


def test_if_nothing() -> None:
    box: list[int] = []

    just(10).if_nothing(lambda: box.append(5))
    assert box == []

    nothing.if_nothing(lambda: box.append(6))
    assert box == [6]
