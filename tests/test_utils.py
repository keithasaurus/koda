from typing import List

from koda.result import err, ok
from koda.safe_try_ import safe_try
from koda.utils import load_once
from tests.utils import assert_same_error_type_with_same_message


def test_load_once() -> None:
    some_list: List[int] = [1, 2, 3]

    def get_last_from_list() -> int:
        return some_list.pop()

    last_elem = load_once(get_last_from_list)

    assert last_elem() == 3
    assert some_list == [1, 2]

    assert last_elem() == 3
    assert some_list == [1, 2]


def test_safe_try() -> None:
    assert safe_try(int, 5) == ok(5)
    assert safe_try(int, 5.0) == ok(5)
    assert_same_error_type_with_same_message(
        safe_try(int, "abc"),
        err(ValueError("invalid literal for int() with base 10: 'abc'")),
    )

    def fail_if_5(val: int) -> int:
        if val == 5:
            raise (Exception("failed"))
        else:
            return val

    assert_same_error_type_with_same_message(
        safe_try(fail_if_5, 5), err(Exception("failed"))
    )


def test_safe_try_with_more_params() -> None:
    def divide_two(a: int, b: int) -> float:
        return a / b

    assert safe_try(divide_two, 4, 2) == ok(2)
    assert_same_error_type_with_same_message(
        safe_try(divide_two, 4, 0), err(ZeroDivisionError("division by zero"))
    )

    def fn3(a: float, b: float, c: float) -> float:
        return a / b / c

    assert safe_try(fn3, 4, 2, 1) == ok(2.0)
    assert_same_error_type_with_same_message(
        safe_try(fn3, 4, 0, 2), err(ZeroDivisionError("division by zero"))
    )

    def fn4(a: float, b: float, c: float, d: str) -> str:
        return f"{a / b / c}{d}"

    assert safe_try(fn4, 4, 2, 1, "F") == ok("2.0F")
    assert_same_error_type_with_same_message(
        safe_try(fn4, 4, 0, 2, "bla"), err(ZeroDivisionError("division by zero"))
    )

    def fn5(a: float, b: float, c: float, d: str, e: bool) -> str:
        assert e
        return f"{a / b / c}{d}"

    assert safe_try(fn5, 4, 2, 1, "F", True) == ok("2.0F")
    assert_same_error_type_with_same_message(
        safe_try(fn5, 4, 0, 2, "bla", False), err(AssertionError("assert False"))
    )

    def fn6(a: float, b: float, c: float, d: str, e: bool, f: bool) -> str:
        assert e and f
        return f"{a / b / c}{d}"

    assert safe_try(fn6, 4, 2, 1, "F", True, True) == ok("2.0F")
    assert_same_error_type_with_same_message(
        safe_try(fn6, 4, 0, 2, "bla", False, True),
        err(AssertionError("assert (False)")),
    )
