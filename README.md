# Koda

Koda is a collection of practical type-safe tools for Python.

At its core are a number of datatypes that are common in functional programming.

## Maybe

`Maybe` is similar to Python's `Optional` type. It has two variants: `Nothing` and `Just`, and they work in similar ways
to what you may have seen in other languages.

```python3
from koda import Maybe, Just, nothing

a: Maybe[int] = Just(5)
b: Maybe[int] = nothing
```

To know if a `Maybe` is a `Just` or a `Nothing`, you'll need to inspect it.

```python3
from koda import Just, Maybe

maybe_str: Maybe[str] = function_returning_maybe_str()

# python 3.10 +
match maybe_str:
    case Just(val):
        print(val)
    case Nothing:
        print("No value!")

# python 3.9 and earlier
if isinstance(maybe_str, Just):
    print(maybe_str.val)
else:
    print("No value!")
```

`Maybe` has methods for conveniently stringing logic together.

#### Maybe.map

```python3
from koda import Just, nothing

def add_10(x: int) -> int:
    return x + 10


Just(5).map(add_10)  # Just(15)
nothing.map(add_10)  # nothing 
Just(5).map(add_10).map(lambda x: f"abc{x}")  # Just("abc15")
```

#### Maybe.flat_map

```python3
from koda import Maybe, Just, nothing


def safe_divide(dividend: int, divisor: int) -> Maybe[float]:
    if divisor != 0:
        return Just(dividend / divisor)
    else:
        return nothing

Just(5).flat_map(lambda x: safe_divide(10, x))  # Just(2)
Just(0).flat_map(lambda x: safe_divide(10, x))  # nothing
nothing.flat_map(lambda x: safe_divide(10, x))  # nothing
```

## Result

`Result` provides a means of representing whether a computation succeeded or failed. To represent success, we can use `OK`;
for failures we can use `Err`. Compared to `Maybe`, `Result` is perhaps most useful in that the "failure" case also returns data,
whereas `Nothing` contains no data.

```python3
from koda import Ok, Err, Result 


def safe_divide_result(dividend: int, divisor: int) -> Result[float, str]:
    if divisor != 0:
        return Ok(dividend / divisor)
    else:
        return Err("cannot divide by zero!")


Ok(5).flat_map(lambda x: safe_divide_result(10, x))  # Ok(2)
Ok(0).flat_map(lambda x: safe_divide_result(10, x))  # Err("cannot divide by zero!") 
Err("some other error").map(lambda x: safe_divide_result(10, x))  # Err("some other error")
```

`Result` can be convenient with `try`/`except` logic.
```python3
from koda import Result, Ok, Err

def divide_by(dividend: int, divisor: int) -> Result[float, ZeroDivisionError]:
    try:
        return Ok(dividend / divisor)
    except ZeroDivisionError as exc:
        return Err(exc)


divided: Result[float, ZeroDivisionError] = divide_by(10, 0)  # Err(ZeroDivisionError("division by zero"))
```

Another way to perform the same computation would be to use `safe_try`:
```python3
from koda import Result, safe_try


# not safe on its own!
def divide(dividend: int, divisor: int) -> float:
    return dividend / divisor

# safe if used with `safe_try`
divided_ok: Result[float, Exception] = safe_try(divide, 10, 2)  # Ok(5)
divided_err: Result[float, Exception] = safe_try(divide, 10, 0)  # Err(ZeroDivisionError("division by zero"))
```

### Conversion between `Result`s, `Maybe`s, and `Optional`s

### Result and Maybe

Convert a `Result` to a `Maybe` type.

```python3
from koda import Just, nothing, Ok, Err

assert Ok(5).to_maybe == Just(5)
assert Err("any error").to_maybe == nothing 
```

Convert a `Maybe` to a `Result` type.

```python3
from koda import Just, nothing, Ok, Err

assert nothing.to_result("value if nothing") == Err("value if nothing")
assert Just(5).to_result("value if nothing") == Ok(5)
```

### `Maybe` and `Optional`

Convert an `Optional` value to a `Maybe`.

```python3
from koda import to_maybe, Just, nothing

assert to_maybe(5) == Just(5)
assert to_maybe("abc") == Just("abc")
assert to_maybe(False) == Just(False)

assert to_maybe(None) == nothing
```

Convert a `Maybe` to an `Optional`.
```python3
from koda import Just, nothing

assert Just(5).to_optional == 5
assert nothing.to_optional is None

# note that `Maybe[None]` will always return None, 
# so `Maybe.get_or_else` would be preferable in this case
assert Just(None) is None
```

### `Result` and `Optional`

Convert an `Optional` value to a `Result`.

```python3
from koda import to_result, Ok, Err 

assert to_result(5, "fallback") == Ok(5)
assert to_result("abc", "fallback") == Ok("abc")
assert to_result(False, "fallback") == Ok(False)

assert to_result(None, "fallback") == Err("fallback")

```

Convert a `Result` to an `Optional`.
```python3
from koda import Ok, Err

assert Ok(5).to_optional == 5
assert Err("some error").to_optional is None

# note that `Result[None, Any]` will always return None, 
# so `Result.get_or_else` would be preferable in this case
assert Ok(None) is None
```

## More

There are many other functions and datatypes included. Some examples:

### compose
Combine functions by sequencing.

```python3
from koda import compose
from typing import Callable

def int_to_str(val: int) -> str:
    return str(val)

def prepend_str_abc(val: str) -> str:
    return f"abc{val}"    

combined_func: Callable[[int], str] = compose(int_to_str, prepend_str_abc)
assert combined_func(10) == "abc10"
```

### mapping_get
Try to get a value from a `Mapping` object, and return an unambiguous result.

```python3
from koda import mapping_get, Just, Maybe, nothing

example_dict: dict[str, Maybe[int]] = {"a": Just(1), "b": nothing}

assert mapping_get(example_dict, "a") == Just(Just(1))
assert mapping_get(example_dict, "b") == Just(nothing)
assert mapping_get(example_dict, "c") == nothing
```

As a comparison, note that `dict.get` can return ambiguous results:
```python
from typing import Optional

example_dict: dict[str, Optional[int]] = {"a": 1, "b": None}

assert example_dict.get("b") is None
assert example_dict.get("c") is None
```
We can't tell from the resulting value whether the `None` was the 
value for a key, or whether the key was not present in the `dict`

### load_once
Create a lazy function, which will only call the passed-in function
the first time it is called. After it is called, the value is cached.
The cached value is returned on each successive call.
```python3
from random import random
from koda import load_once

call_random_once = load_once(random)  # has not called random yet

retrieved_val: float = call_random_once()
assert retrieved_val == call_random_once()
```

## Intent

Koda is intended to focus on a small set of practical data types and utility functions for Python. It will not 
grow to encompass every possible functional or typesafe concept. Similarly, the intent of this library is to avoid 
requiring extra plugins (beyond a type-checker like mypy or pyright) or specific typchecker settings. As such,
it is unlikely that things like Higher Kinded Types emulation or extended type inference will be implemented in this 
library.
