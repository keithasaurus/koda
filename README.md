# Koda

Koda is a collection of practical type-safe tools for Python.

At it's core are a number of datatypes that are common in functional programming.

## Maybe

`Maybe` is similar to Python's `Optional` type. It has two variants: `Nothing` and `Just`, and they work in similar ways
to what you may have seen in other languages.

```python3
from koda.maybe import Maybe, Just, Nothing

a: Maybe[int] = Just(5)
b: Maybe[int] = Nothing
```

`Maybe` has methods for conveniently stringing logic together.

#### map

```python3
from koda.maybe import Just, Nothing

Just(5).map(lambda x: x + 10)  # Just(15)
Nothing.map(lambda x: x + 10)  # Nothing
```

#### flat_map

```python3
from koda.maybe import Maybe, Just, Nothing


def divide_by(dividend: int, divisor: int) -> Maybe[float]:
    return Just(dividend / divisor) if divisor != 0 else Nothing


Just(5).flat_map(lambda x: divide_by(10, x))  # Just(2)
Just(0).flat_map(lambda x: divide_by(10, x))  # Nothing
Nothing.map(lambda x: divide_by(10, x))  # Nothing
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

One of the main reasons you might want to 



The main difference is that its `NothingType` is unambiguous. To illustrate the point, consider how
Python's `dict.get(...)` works.

```python3
from typing import Optional

example_dict: dict[str, Optional[str]] = {"a": None, "b": "ok"}

a_val: Optional[str] = example_dict.get("a")
assert a_val is None
c_val: Optional[str] = example_dict.get("c")
assert c_val is None
```

In the example above, if we look at `a_val` and `c_val`, we cannot tell which keys existed in the original map.

In koda, we could use `get_mapping_val` to get an unambiguous result:

```python3
from typing import Optional
from koda import mapping_get
from koda.maybe import Nothing, Just

example_dict: dict[str, Optional[str]] = {"a": None, "b": "ok"}

assert mapping_get("a")(example_dict) == Just(None)
assert mapping_get("c")(example_dict) == Nothing
```

In this case, we can tell that `None` was set as the value for key "a" and 
