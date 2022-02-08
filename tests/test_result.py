from koda.result import Err, Ok
from tests.utils import enforce_functor_one_val, enforce_monad_unit, enforce_monad_flat_map, enforce_applicative_apply


def test_result() -> None:
    enforce_functor_one_val(Ok, "map")
    enforce_monad_unit(Ok)
    enforce_monad_flat_map(Ok, Err("something went wrong"))
    enforce_applicative_apply(Ok, Err("something went wrong"))
    assert Ok("whatever").ok()
    assert not Err("whatever").ok()
