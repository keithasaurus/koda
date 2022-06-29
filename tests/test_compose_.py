from typing import Union

from koda import Result
from koda._generics import A, B
from koda.compose_ import compose


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


def _to_char_list(s: str) -> list[str]:
    return [c for c in s]


def _to_char_tuple(s: list[str]) -> tuple[str, ...]:
    return tuple(s)


def _reverse_tuple(s: tuple[str, ...]) -> tuple[str, ...]:
    return s[::-1]


def _get_result_val(data: Result[A, B]) -> Union[A, B]:
    return data.variant.val


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
