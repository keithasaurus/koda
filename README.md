# Koda

Koda is a collection of type-safe tools for Python. One particular area
of focus is on validation of Json data.

## JSON Validation

Koda aims to make it easy (and non-magical) to build validators. To that end
it provides combinable validators, which return validated (and possibly transformed)
data when valid; and strucured error messages on failure. They can also be 
used to define OpenAPI schemas out of the box. 

### Quickstart

Let's make a simple person validator.

```python
from dataclasses import dataclass

from koda.json.validation import Obj2, String, Integer, MinLength, Minimum, prop


# a class we can instantiate with valid data 
@dataclass
class Person:
    name: str
    age: int


person_validator = Obj2( 
    prop("name", String(MinLength(1))),
    prop("age", Integer(Minimum(0))),
    into=Person
)
```

We can now send in data to the validator and get appropriate responses.

```python
from koda.result import Ok

assert person_validator({"name": "bob", "age": 25}) == Ok(Person("bob", 25))
```
Great, a valid example gives us a `Person`! Note that it's wrapped in an `Ok` object. 
This explicitly tells us the result was successful. Let's see what happens if it fails.

```python
bad_age_result = person_validator({"name": "bob", "age": -100})
assert bad_age_result == v.err({"age": ["minimum allowed value is 0"]})
```
In the case of invalid data, we return a `Err` object. note that `err` here is a 
simple helper function that allows for easier reading. To demonstrate why,
the  actual value looks like this:

```python
Error(val=Jsonable(val={'age': Jsonable(val=[Jsonable(val='minimum allowed value is 0')])}))
```
This verbose `Jsonable` type exists because of current limitations in mypy's typechecking.

Finally, we can generate OpenAPI schemas from our validators.

```python
from koda.json.openapi import generate_schema

assert generate_schema("Person", person_validator) == {
    "Person": {
        "type": "object",
        "additionalProperties": False,
        "required": ["name", "age"],
        "properties": {
            "name": {
                "type": "string",
                "minLength": 1
            },
            "age": {
                "type": "integer",
                "minimum": 0,
                "exclusiveMinimum": False
            }
        }
    }
}
```