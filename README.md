# Koda

Koda is a collection of practical type-safe tools for Python.

At it's core are a number of datatypes that are common in functional programming.

## Maybe
`Maybe` is similar to Python's `Optional` type. It has two variants: `Nothing` and `Just`, and they work in similar
ways to other languages.
```python3
from koda.maybe import Maybe, Just, Nothing

a: Maybe[int] == Just(5)
b: Maybe[int] == Nothing
```

`Maybe` has methods for convenience stringing together logic.
```python3

```



The main difference is that 
its `NothingType` is unambiguous. To illustrate the point, consider how Python's `dict.get(...)`  works.  

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
