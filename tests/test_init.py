from dataclasses import dataclass
from typing import List, Tuple, TypeVar, Union, Optional

from koda import compose, load_once, maybe_to_result, result_to_maybe, safe_try, mapping_get
from koda.maybe import Just, Nothing
from koda.result import Err, Result, Ok
from tests.utils import assert_same_error_type_with_same_message

A = TypeVar("A")
B = TypeVar("B")


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


def test_maybe_to_result() -> None:
    @dataclass
    class SomeError:
        msg: str
        params: List[str]

    fail_message = SomeError("it failed", ["a", "b"])
    fn = maybe_to_result(fail_message)

    assert fn(Just(5)) == Ok(5)

    assert fn(Nothing) == Err(fail_message)


def test_result_to_maybe() -> None:
    assert result_to_maybe(Ok(3)) == Just(3)
    assert result_to_maybe(Err("something")) == Nothing


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
    assert safe_try(int)(5) == Ok(5)
    assert safe_try(int)(5.0) == Ok(5)
    assert_same_error_type_with_same_message(
        safe_try(int)("abc"),
        Err(ValueError("invalid literal for int() with base 10: 'abc'")),
    )

    def fail_if_5(val: int) -> int:
        if val == 5:
            raise (Exception("failed"))
        else:
            return val

    assert_same_error_type_with_same_message(
        safe_try(fail_if_5)(5), Err(Exception("failed"))
    )


def test_mapping_get():
    d: dict[str, Optional[str]] = {"a": None, "b": "ok"}

    assert mapping_get(d, "a") == Just(None)
    assert mapping_get(d, "b") == Just("ok")
    assert mapping_get(d, "c") == Nothing
