from random import random
from typing import Callable, Dict, Optional

from koda import (
    Err,
    Just,
    Maybe,
    Ok,
    Result,
    compose,
    load_once,
    mapping_get,
    nothing,
    safe_try,
    to_maybe,
)


def str_to_int(a: str) -> Maybe[int]:
    try:
        int_val = int(a)
    except ValueError:
        return nothing
    else:
        return Just(int_val)


x = str_to_int("5").map(str).get_or_else("ok")


a: Maybe[int] = Just(5)
b: Maybe[int] = nothing


def function_returning_maybe_str() -> Maybe[str]:
    if random() > 0.5:
        return Just("ok")
    else:
        return nothing


maybe_str: Maybe[str] = function_returning_maybe_str()

if isinstance(maybe_str, Just):
    print(maybe_str.val)
else:
    print("No value!")

# todo: extract to py3.10-only file
# match maybe_str:
#     case Just(val):
#         print(val)
#     case Nothing:
#         print("No value!")
#


def int_add_10(x: int) -> int:
    return x + 10


Just(5).map(int_add_10)  # Just(15)
nothing.map(int_add_10)  # Nothing
Just(5).map(int_add_10).map(lambda x: f"abc{x}")  # Just("abc15")


def safe_divide(dividend: int, divisor: int) -> Maybe[float]:
    if divisor != 0:
        return Just(dividend / divisor)
    else:
        return nothing


Just(5).flat_map(lambda x: safe_divide(10, x))  # Just(2)
Just(0).flat_map(lambda x: safe_divide(10, x))  # Nothing
nothing.flat_map(lambda x: safe_divide(10, x))  # Nothing


def safe_divide_result(dividend: int, divisor: int) -> Result[float, str]:
    if divisor != 0:
        return Ok(dividend / divisor)
    else:
        return Err("cannot divide by zero!")


Ok(5).flat_map(lambda x: safe_divide_result(10, x))  # Ok(2)
Ok(0).flat_map(lambda x: safe_divide_result(10, x))  # Err("cannot divide by zero!")
Err("some other error").map(
    lambda x: safe_divide_result(10, x)
)  # Err("some other error")


def divide_by(dividend: int, divisor: int) -> Result[float, ZeroDivisionError]:
    try:
        return Ok(dividend / divisor)
    except ZeroDivisionError as exc:
        return Err(exc)


divided: Result[float, ZeroDivisionError] = divide_by(
    10, 0
)  # Err(ZeroDivisionError("division by zero"))


# not safe on its own!
def divide(dividend: int, divisor: int) -> float:
    return dividend / divisor


# safe if used with `safe_try`
divided_ok: Result[float, Exception] = safe_try(divide, 10, 2)  # Ok(5)
divided_err: Result[float, Exception] = safe_try(
    divide, 10, 0
)  # Err(ZeroDivisionError("division by zero"))


def int_to_str(val: int) -> str:
    return str(val)


def prepend_str_abc(val: str) -> str:
    return f"abc{val}"


combined_func: Callable[[int], str] = compose(int_to_str, prepend_str_abc)
assert combined_func(10) == "abc10"


example_dict: Dict[str, Maybe[int]] = {"a": Just(1), "b": nothing}

assert mapping_get(example_dict, "a") == Just(Just(1))
assert mapping_get(example_dict, "b") == Just(nothing)
assert mapping_get(example_dict, "c") == nothing


example_dict_1: Dict[str, Optional[int]] = {"a": 1, "b": None}

assert example_dict_1.get("b") is None
assert example_dict_1.get("c") is None


call_random_once = load_once(random)  # has not called random yet

retrieved_val: float = call_random_once()
assert retrieved_val == call_random_once()

assert nothing.to_result("value if nothing") == Err("value if nothing")
assert Just(5).to_result("value if nothing") == Ok(5)


assert Ok(5).to_maybe == Just(5)
assert Err("any error").to_maybe == nothing

assert to_maybe(5) == Just(5)
assert to_maybe("abc") == Just("abc")
assert to_maybe(False) == Just(False)

assert to_maybe(None) == nothing


def add_5(x: int) -> int:
    return x + 5


x1: Optional[int] = Just(5).map(add_5).to_result("failed!").to_optional
x2: Optional[int] = nothing.map(add_5).to_result("failed!").to_optional
