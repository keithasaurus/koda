from random import random
from typing import Callable, Optional

from koda import (
    Just,
    Maybe,
    Result,
    load_once,
    mapping_get,
    maybe_to_result,
    nothing,
    result_to_maybe,
    safe_try,
    to_maybe,
)
from koda.compose_ import compose
from koda.maybe import just
from koda.result import err, ok


def str_to_int(a: str) -> Maybe[int]:
    try:
        int_val = int(a)
    except ValueError:
        return nothing
    else:
        return just(int_val)


x = str_to_int("5").map(str).get_or_else("ok")


a: Maybe[int] = just(5)
b: Maybe[int] = nothing


def function_returning_maybe_str() -> Maybe[str]:
    if random() > 0.5:
        return just("ok")
    else:
        return nothing


maybe_str: Maybe[str] = function_returning_maybe_str()

if isinstance(maybe_str.variant, Just):
    print(maybe_str.variant.val)
else:
    print("No value!")


# match maybe_str.val:
#     case Just(val):
#         print(val)
#     case Nothing:
#         print("No value!")


def int_add_10(x: int) -> int:
    return x + 10


just(5).map(int_add_10)  # Just(15)
nothing.map(int_add_10)  # Nothing
just(5).map(int_add_10).map(lambda x: f"abc{x}")  # Just("abc15")


def safe_divide(dividend: int, divisor: int) -> Maybe[float]:
    if divisor != 0:
        return just(dividend / divisor)
    else:
        return nothing


just(5).flat_map(lambda x: safe_divide(10, x))  # Just(2)
just(0).flat_map(lambda x: safe_divide(10, x))  # Nothing
nothing.flat_map(lambda x: safe_divide(10, x))  # Nothing


def safe_divide_result(dividend: int, divisor: int) -> Result[float, str]:
    if divisor != 0:
        return ok(dividend / divisor)
    else:
        return err("cannot divide by zero!")


ok(5).flat_map(lambda x: safe_divide_result(10, x))  # ok(2)
ok(0).flat_map(lambda x: safe_divide_result(10, x))  # err("cannot divide by zero!")
err("some other error").map(
    lambda x: safe_divide_result(10, x)
)  # err("some other error")


def divide_by(dividend: int, divisor: int) -> Result[float, ZeroDivisionError]:
    try:
        return ok(dividend / divisor)
    except ZeroDivisionError as exc:
        return err(exc)


divided: Result[float, ZeroDivisionError] = divide_by(
    10, 0
)  # err(ZeroDivisionError("division by zero"))


# not safe on its own!
def divide(dividend: int, divisor: int) -> float:
    return dividend / divisor


# safe if used with `safe_try`
divided_ok: Result[float, Exception] = safe_try(divide, 10, 2)  # ok(5)
divided_err: Result[float, Exception] = safe_try(
    divide, 10, 0
)  # err(ZeroDivisionError("division by zero"))


def int_to_str(val: int) -> str:
    return str(val)


def prepend_str_abc(val: str) -> str:
    return f"abc{val}"


combined_func: Callable[[int], str] = compose(int_to_str, prepend_str_abc)
assert combined_func(10) == "abc10"


example_dict: dict[str, Maybe[int]] = {"a": just(1), "b": nothing}

assert mapping_get(example_dict, "a") == just(just(1))
assert mapping_get(example_dict, "b") == just(nothing)
assert mapping_get(example_dict, "c") == nothing


example_dict_1: dict[str, Optional[int]] = {"a": 1, "b": None}

assert example_dict_1.get("b") is None
assert example_dict_1.get("c") is None


call_random_once = load_once(random)  # has not called random yet

retrieved_val: float = call_random_once()
assert retrieved_val == call_random_once()

assert maybe_to_result("value if nothing", nothing) == err("value if nothing")
assert maybe_to_result("value if nothing", just(5)) == ok(5)


assert result_to_maybe(ok(5)) == just(5)
assert result_to_maybe(err("any error")) == nothing

assert to_maybe(5) == just(5)
assert to_maybe("abc") == just("abc")
assert to_maybe(False) == just(False)

assert to_maybe(None) == nothing
