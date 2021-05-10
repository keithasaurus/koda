from dataclasses import dataclass

import koda.json.validation as v
from koda.json.openapi import generate_schema
from koda.result import Ok


@dataclass
class Person:
    name: str
    age: int


person_validator = v.Obj2(
    v.prop("name", v.String(v.MinLength(1))),
    v.prop("age", v.Integer(v.Minimum(0))),
    into=Person,
)

# valid example
result_1 = person_validator({"name": "bob", "age": 25})
assert result_1 == Ok(Person("bob", 25))

# invalid examples
bad_age_result = person_validator({"name": "bob", "age": -100})
assert bad_age_result == v.err({"age": ["minimum allowed value is 0"]})

multiple_errors_result = person_validator({"age": 25.5})
assert multiple_errors_result == v.err(
    {"name": ["key missing"], "age": ["expected an integer"]}
)

# as openapi schema
assert generate_schema("Person", person_validator) == {
    "Person": {
        "type": "object",
        "additionalProperties": False,
        "required": ["name", "age"],
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "age": {"type": "integer", "minimum": 0, "exclusiveMinimum": False},
        },
    }
}
