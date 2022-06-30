from typing import Any

from koda import Err, Ok
from koda.maybe import Just, Nothing, nothing
from tests.utils import (
    enforce_applicative_apply,
    enforce_functor_one_val,
    enforce_monad_flat_map,
    enforce_monad_unit,
)


def test_maybe() -> None:
    enforce_functor_one_val(Just, "map")
    enforce_monad_unit(Just)
    enforce_monad_flat_map(Just, nothing)
    enforce_applicative_apply(Just, nothing)


def test_nothing_map() -> None:
    def anything_to_5(_: Any) -> int:
        return 5

    assert nothing.map(anything_to_5) == nothing


def test_get_or_else() -> None:
    assert Just(5).get_or_else(12) == 5
    assert nothing.get_or_else(12) == 12


def test_to_optional() -> None:
    assert Just(2).to_optional == 2
    assert Just(None).to_optional is None
    assert nothing.to_optional is None


def test_to_result() -> None:
    assert Just(2).to_result("error!") == Ok(2)
    assert nothing.to_result("error!") == Err("error!")


def test_nothing_singleton() -> None:
    assert nothing is Nothing()
