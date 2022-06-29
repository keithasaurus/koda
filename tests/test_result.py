from typing import Any

from koda.result import Ok, Result, err, ok
from tests.utils import (
    enforce_applicative_apply,
    enforce_functor_one_val,
    enforce_monad_flat_map,
    enforce_monad_unit,
)


def test_result() -> None:
    enforce_functor_one_val(Ok, "map")
    enforce_monad_unit(Ok)
    enforce_monad_flat_map(Ok, err("something went wrong"))
    enforce_applicative_apply(Ok, err("something went wrong"))


def test_ok_flat_map_err() -> None:
    def add_one(val: int) -> Result[int, str]:
        return err(str(val) + "ok")

    result: Result[int, str] = ok(5).flat_map_err(add_one)
    assert result == ok(5)


def test_ok_map_err() -> None:
    def str_twice(val: str) -> str:
        return f"{val}{val}"

    assert ok(5).map_err(str_twice) == ok(5)


def test_ok_swap() -> None:
    assert ok(5).swap() == err(5)


def test_err_map() -> None:
    def return_25(a: Any) -> int:
        return 25

    assert err(3).map(return_25) == err(3)


def test_err_flat_map_err() -> None:
    def add_one(val: int) -> Result[str, int]:
        return err(val + 1)

    result: Result[str, int] = err(5).flat_map_err(add_one)
    assert result == err(6)


def test_err_map_err() -> None:
    def _int_to_str(n: int) -> str:
        return str(n)

    result: Result[bool, str] = err(5).map_err(_int_to_str)
    assert result == err("5")


def test_err_swap() -> None:
    assert err(3).swap() == ok(3)


def test_get_or_else() -> None:
    assert ok(5).get_or_else(12) == 5
    assert err("some error").get_or_else(12) == 12
