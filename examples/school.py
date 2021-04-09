from dataclasses import dataclass
from typing import List

from koda.either import Either
from koda.json.validation import (ArrayOf, Integer, NotBlank, Nullable, Obj2, Obj4,
                                  OneOf2, String, key, not_blank, unwrap_jsonable)
from koda.maybe import Maybe
from koda.result import Failure


@dataclass
class Person:
    name: str
    age: Maybe[int]


@dataclass
class School:
    name: str
    country: str
    principal: Maybe[Person]
    grades: List[Either[int, str]]


person_validator = Obj2(
    key("name", String(not_blank)),
    key("age", Nullable(Integer())),
    into=Person
)

school_validator = Obj4(
    key("name",
        String(not_blank)),
    key("country",
        String(not_blank)),
    key("principal",
        Nullable(person_validator)),
    key("grades",
        ArrayOf(OneOf2(Integer(),
                       String(NotBlank())))),
    into=School
)


@dataclass
class House:
    stories: int
    lot_square_feet: int


house_validator = Obj2(
    key("stories", Integer()),
    key("lot_square_feet", Integer()),
    into=House
)

buildings_validator = ArrayOf(
    OneOf2(("school variant", school_validator),
           ("house variant", house_validator))
)

result = buildings_validator(
    [
        {"name": "a school",
         "country": "United States",
         "principal": {"name": "Something"},
         "grades": [1, 2, 3, "something"]},
        {"stories": 1,
         "lot_square_feet": 4000}
    ]
)

if isinstance(result, Failure):
    print(unwrap_jsonable(result.val))
else:
    print(result)
