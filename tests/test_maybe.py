from koda.maybe import Just, Nothing
from koda.utils.test import (
    enforce_applicative_apply,
    enforce_functor_one_val,
    enforce_monad_flat_map,
    enforce_monad_unit,
)


def test_maybe() -> None:
    enforce_functor_one_val(Just, "map")
    enforce_monad_unit(Just)
    enforce_monad_flat_map(Just, Nothing)
    enforce_applicative_apply(Just, Nothing)
