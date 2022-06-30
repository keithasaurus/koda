from typing import Any

from koda.maybe import Just, nothing
from koda.result import Err, Ok, Result
from tests.utils import (
    enforce_applicative_apply,
    enforce_functor_one_val,
    enforce_monad_flat_map,
    enforce_monad_unit,
)


def test_result() -> None:
    enforce_functor_one_val(Ok, "map")
    enforce_monad_unit(Ok)
    enforce_monad_flat_map(Ok, Err("something went wrong"))
    enforce_applicative_apply(Ok, Err("something went wrong"))


def test_ok_flat_map_err() -> None:
    def add_one(val: int) -> Result[int, str]:
        return Err(str(val) + "ok")

    result: Result[int, str] = Ok(5).flat_map_err(add_one)
    assert result == Ok(5)


def test_ok_map_err() -> None:
    def str_twice(val: str) -> str:
        return f"{val}{val}"

    assert Ok(5).map_err(str_twice) == Ok(5)


def test_ok_swap() -> None:
    assert Ok(5).swap() == Err(5)


def test_err_map() -> None:
    def return_25(a: Any) -> int:
        return 25

    assert Err(3).map(return_25) == Err(3)


def test_err_flat_map_err() -> None:
    def add_one(val: int) -> Result[str, int]:
        return Err(val + 1)

    result: Result[str, int] = Err(5).flat_map_err(add_one)
    assert result == Err(6)


def test_err_map_err() -> None:
    def _int_to_str(n: int) -> str:
        return str(n)

    result: Result[bool, str] = Err(5).map_err(_int_to_str)
    assert result == Err("5")


def test_err_swap() -> None:
    assert Err(3).swap() == Ok(3)


def test_get_or_else() -> None:
    assert Ok(5).get_or_else(12) == 5
    assert Err("some error").get_or_else(12) == 12


def test_to_maybe() -> None:
    assert Ok(123).to_maybe == Just(123)
    assert Ok(None).to_maybe == Just(None)
    assert Err("some error").to_maybe == nothing


def test_to_optional() -> None:
    assert Ok(123).to_optional == 123
    assert Ok(None).to_optional is None
    assert Err("some error").to_optional is None
