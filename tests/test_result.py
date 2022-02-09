from koda.result import Err, Ok, Result
from tests.utils import enforce_functor_one_val, enforce_monad_unit, \
    enforce_monad_flat_map, enforce_applicative_apply
from typing import Any


def test_result() -> None:
    enforce_functor_one_val(Ok, "map")
    enforce_monad_unit(Ok)
    enforce_monad_flat_map(Ok, Err("something went wrong"))
    enforce_applicative_apply(Ok, Err("something went wrong"))


def test_ok_flat_map_err() -> None:
    def add_one(val: int) -> Result[int, Any]:
        return Err(val + 1)

    assert Ok(5).flat_map_err(add_one) == Ok(5)


def test_ok_map_err() -> None:
    def str_twice(val: str) -> str:
        return f"{val}{val}"

    assert Ok(5).map_err(str_twice) == Ok(5)


def test_ok_swap() -> None:
    assert Ok(5).swap() == Err(5)


def test_err_map() -> None:
    assert Err(3).map(lambda _: 25) == Err(3)


def test_err_flat_map_err() -> None:
    def add_one(val: int) -> Result[str, int]:
        return Err(val + 1)

    assert Err(5).flat_map_err(add_one) == Err(6)


def test_err_map_err() -> None:
    def _int_to_str(n: int) -> str:
        return str(n)

    assert Err(5).map_err(_int_to_str) == Err('5')


def test_err_swap() -> None:
    assert Err(3).swap() == Ok(3)
