from typing import Dict, List, Optional, Tuple, Union

from koda._generics import A, B
from koda.maybe import Just, nothing
from koda.result import Err, Ok, Result
from koda.utils import (
    always,
    compose,
    load_once,
    mapping_get,
    safe_try,
    to_maybe,
    to_result,
)
from tests.utils import assert_same_error_type_with_same_message


def _halve(f: float) -> float:
    return f / 2.0


def _float_to_int(f: float) -> int:
    return round(f)


def _inc(n: int) -> int:
    return n + 1


def _int_to_str(n: int) -> str:
    return str(n)


def _prepend_a(s: str) -> str:
    return f"a{s}"


def _to_char_list(s: str) -> List[str]:
    return [c for c in s]


def _to_char_tuple(s: List[str]) -> Tuple[str, ...]:
    return tuple(s)


def _reverse_tuple(s: Tuple[str, ...]) -> Tuple[str, ...]:
    return s[::-1]


def _get_result_val(data: Result[A, B]) -> Union[A, B]:
    return data.val


def test_compose2() -> None:
    composed_func = compose(_halve, _float_to_int)
    assert composed_func(7.3) == 4


def test_compose3() -> None:
    composed_func = compose(_halve, _float_to_int, _inc)
    assert composed_func(7.3) == 5


def test_compose4() -> None:
    composed_func = compose(_halve, _float_to_int, _inc, _int_to_str)
    assert composed_func(7.3) == "5"


def test_compose5() -> None:
    composed_func = compose(_halve, _float_to_int, _inc, _int_to_str, _prepend_a)
    assert composed_func(7.3) == "a5"


def test_compose6() -> None:
    composed_func = compose(
        _halve, _float_to_int, _inc, _int_to_str, _prepend_a, _to_char_list
    )
    assert composed_func(7.3) == ["a", "5"]


def test_compose7() -> None:
    composed_func = compose(
        _halve,
        _float_to_int,
        _inc,
        _int_to_str,
        _prepend_a,
        _to_char_list,
        _to_char_tuple,
    )
    assert composed_func(7.3) == ("a", "5")


def test_compose8() -> None:
    composed_func = compose(
        _halve,
        _float_to_int,
        _inc,
        _int_to_str,
        _prepend_a,
        _to_char_list,
        _to_char_tuple,
        _reverse_tuple,
    )
    assert composed_func(7.3) == ("5", "a")


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
    assert safe_try(int, 5) == Ok(5)
    assert safe_try(int, 5.0) == Ok(5)
    assert_same_error_type_with_same_message(
        safe_try(int, "abc"),
        Err(ValueError("invalid literal for int() with base 10: 'abc'")),
    )

    def fail_if_5(val: int) -> int:
        if val == 5:
            raise (Exception("failed"))
        else:
            return val

    assert_same_error_type_with_same_message(
        safe_try(fail_if_5, 5), Err(Exception("failed"))
    )


def test_safe_try_with_more_params() -> None:
    def divide_two(a: int, b: int) -> float:
        return a / b

    assert safe_try(divide_two, 4, 2) == Ok(2)
    assert_same_error_type_with_same_message(
        safe_try(divide_two, 4, 0), Err(ZeroDivisionError("division by zero"))
    )

    def fn3(a: float, b: float, c: float) -> float:
        return a / b / c

    assert safe_try(fn3, 4, 2, 1) == Ok(2.0)
    assert_same_error_type_with_same_message(
        safe_try(fn3, 4, 0, 2), Err(ZeroDivisionError("division by zero"))
    )

    def fn4(a: float, b: float, c: float, d: str) -> str:
        return f"{a / b / c}{d}"

    assert safe_try(fn4, 4, 2, 1, "F") == Ok("2.0F")
    assert_same_error_type_with_same_message(
        safe_try(fn4, 4, 0, 2, "bla"), Err(ZeroDivisionError("division by zero"))
    )

    def fn5(a: float, b: float, c: float, d: str, e: bool) -> str:
        assert e
        return f"{a / b / c}{d}"

    assert safe_try(fn5, 4, 2, 1, "F", True) == Ok("2.0F")
    assert_same_error_type_with_same_message(
        safe_try(fn5, 4, 0, 2, "bla", False), Err(AssertionError("assert False"))
    )

    def fn6(a: float, b: float, c: float, d: str, e: bool, f: bool) -> str:
        assert e and f
        return f"{a / b / c}{d}"

    assert safe_try(fn6, 4, 2, 1, "F", True, True) == Ok("2.0F")
    assert_same_error_type_with_same_message(
        safe_try(fn6, 4, 0, 2, "bla", False, True),
        Err(AssertionError("assert (False)")),
    )


def test_mapping_get() -> None:
    d: Dict[str, Optional[str]] = {"a": None, "b": "ok"}

    assert mapping_get(d, "a") == Just(None)
    assert mapping_get(d, "b") == Just("ok")
    assert mapping_get(d, "c") == nothing


def test_to_maybe() -> None:
    assert to_maybe(5) == Just(5)
    assert to_maybe("abc") == Just("abc")
    assert to_maybe(False) == Just(False)

    assert to_maybe(None) == nothing


def test_to_result() -> None:
    assert to_result(5, "fallback") == Ok(5)
    assert to_result("abc", "fallback") == Ok("abc")
    assert to_result(False, "fallback") == Ok(False)

    assert to_result(None, "fallback") == Err("fallback")


def test_always() -> None:
    fn = always(5)
    assert fn() == 5
    assert fn(1, 2, 3, arg=12) == 5
