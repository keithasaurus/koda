from typing import Any

from koda.maybe import Just, nothing
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
