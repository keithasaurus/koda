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

import koda.json.validation as v


# a class we can instantiate with valid data 
@dataclass
class Person:
    name: str
    age: int


person_validator = v.Obj2( 
    v.prop("name", v.String(v.MinLength(1))),
    v.prop("age", v.Integer(v.Minimum(0))),
    into=Person
)
```

We can now send in data to the validator and get appropriate responses.

```python
from koda.result import Ok

result_1 = person_validator({"name": "bob", "age": 25})
assert result_1 == Ok(Person("bob", 25))
```
Great, a valid example gives us a person! Note that it's wrapped in a `Success` object. 
This explicitly tells us the result was successful. Let's see what happens if it fails.

```python
bad_age_result = person_validator({"name": "bob", "age": -100})
assert bad_age_result == v.err({"age": ["minimum allowed value is 0"]})
```
In the case of failures, we return a `Failure` object. note that `fail` here is a 
simple helper function that allows for easier reading in most cases. To demonstrate why,
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