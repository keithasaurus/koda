# Koda

Koda is a collection of practical type-safe tools for Python.

At it's core are a number of datatypes that are common in functional programming.

## Maybe

`Maybe` is similar to Python's `Optional` type. It has two variants: `Nothing` and `Just`, and they work in similar ways
to what you may have seen in other languages.

```python3
from koda.maybe import Maybe, Just, nothing

a: Maybe[int] = Just(5)
b: Maybe[int] = nothing
```

To know if a `Maybe` is a `Just` or a `Nothing`, you'll need to inspect it.

```python3
from koda.maybe import Just, Maybe, Nothing

maybe_random_val: Maybe[str] = some_function_that_returns_maybe_str()

# unwrap by checking instance type
if isinstance(maybe_random_val, Just):
    print(maybe_random_val.val)
else:
    print("No value!")

# unwrap with structural pattern matching (python 3.10 +)
match maybe_random_val:
    case Just(val):
        print(val)
    case Nothing:
        print("No value!")
```

`Maybe` has methods for conveniently stringing logic together.

#### Maybe.map

```python3
from koda.maybe import Just, nothing

Just(5).map(lambda x: x + 10)  # Just(15)
nothing.map(lambda x: x + 10)  # Nothing
Just(5).map(lambda x: x + 10).map(lambda x: f"abc{x}")  # Just("abc15")
```

#### Maybe.flat_map

```python3
from koda.maybe import Maybe, Just, nothing


def divide_by(dividend: int, divisor: int) -> Maybe[float]:
    return Just(dividend / divisor) if divisor != 0 else nothing


Just(5).flat_map(lambda x: divide_by(10, x))  # Just(2)
Just(0).flat_map(lambda x: divide_by(10, x))  # Nothing
nothing.map(lambda x: divide_by(10, x))  # Nothing
```

## Result

`Result` provides a means to represent whether a computation succeeded or failed. For these two scenarios, we have the classes
`Ok` and `Err`. Compared to `Maybe`, `Result` is perhaps most useful in that the "failure" case also returns data.
```python3
from koda.result import Ok, Err, Result 


def divide_by(dividend: int, divisor: int) -> Result[float, str]:
    return Ok(dividend / divisor) if divisor != 0 else Err("cannot divide by zero!") 


Ok(5).flat_map(lambda x: divide_by(10, x))  # Ok(2)
Ok(0).flat_map(lambda x: divide_by(10, x))  # Err("cannot divide by zero!") 
Err("some other error").map(lambda x: divide_by(10, x))  # Err("some other error")
```

`Result` can be convenient with `try`/`except` logic.
```python3
from koda.result import Result, Ok, Err

def divide_by(dividend: int, divisor: int) -> Result[float, ZeroDivisionError]:
    try:
        return Ok(dividend / divisor)
    except ZeroDivisionError as exc:
        return Err(exc)


divided: Result[float, ZeroDivisionError] = divide_by(10, 0)  # Err(ZeroDivisionError("division by zero"))
```

A different way to perform the same computation would be to use `safe_try`
from koda.result import Result, Ok, Err

```python3
from koda.result import Result
from koda import safe_try


def divide_by(dividend: int, divisor: int) -> float:
    return dividend / divisor

safe_divide_by = safe_try(divide_by)

divided: Result[float, ZeroDivisionError] = divide_by(10, 0)  # Err(ZeroDivisionError("division by zero"))
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

def prepend_str_abc(val: str) -> str
    return f"abc{val}"    

combined_func: Callable[[int], str] = compose(lambda x: x + 5, int_to_str, prepend_str_abc)
assert combined_func(10) == "abc15"
```

### mapping_get
Try to get a value from a `Mapping` object, and return an unambiguous result.

```python3
from koda import mapping_get
from koda.maybe import Just, Maybe, nothing

example_dict: dict[str, Maybe[int]] = {"a": Just(1), "b": nothing}

assert mapping_get(example_dict, "a") == Just(Just(1))
assert mapping_get(example_dict, "b") == Just(nothing)
assert mapping_get(example_dict, "c") == nothing
```

### load_once
Execute a function the first time it's called, cache the result, and return the cached result
for every successive call.
```python3
from random import random
from koda import load_once

call_random_once = load_once(random)  # has not called random yet
assert call_random_once() == call_random_once() == call_random_once()
```

### maybe_to_result

Convert a `Maybe` to a `Result` type.

```python3
from koda import maybe_to_result
from koda.maybe import Just, nothing
from koda.result import Ok, Err

assert maybe_to_result("bad result", Just(5)) == Ok(5)
assert maybe_to_result("bad result", nothing) == Err("bad result") 
```

### result_to_maybe

Convert a `Result` to a `Maybe` type.

```python3
from koda import result_to_maybe
from koda.maybe import Just, nothing
from koda.result import Ok, Err

assert result_to_maybe(Ok(5)) == Just(5)
assert result_to_maybe(Err("any error")) == nothing 
```

## Intent

This library is intended to focus on a small set of practical data types and utility functions for Python. It will not 
grow to encompass every possible functional or typesafe concept. Similarly, the intent of this library is to avoid 
requiring extra plugins (beyond a type-checker like mypy or pyright) or specific typchecker settings. 
