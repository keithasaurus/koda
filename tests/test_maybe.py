from koda.maybe import Just, nothing
from tests.utils import enforce_functor_one_val, enforce_monad_unit, \
    enforce_monad_flat_map, enforce_applicative_apply


def test_maybe() -> None:
    enforce_functor_one_val(Just, "map")
    enforce_monad_unit(Just)
    enforce_monad_flat_map(Just, nothing)
    enforce_applicative_apply(Just, nothing)


def test_nothing_map() -> None:
    assert nothing.map(lambda _: 5) == nothing
