import re
from dataclasses import dataclass
from datetime import date
from typing import List, Set, TypeVar

import koda.json.validation as v
from koda.either import First, Second, Third
from koda.json.openapi import generate_schema
from koda.maybe import Just, Maybe, Nothing
from koda.result import Success

A = TypeVar('A')
Ret = TypeVar('Ret')


def test_recursive_validator() -> None:
    @dataclass
    class Comment:
        name: str
        replies: List['Comment']  # noqa: F821

    def get_comment_recur() -> v.Obj2[str, List[Comment], Comment]:
        return comment_validator

    comment_validator: v.Obj2[str, List[Comment], Comment] = v.Obj2(
        v.key('name', v.String(v.not_blank)),
        v.key('replies', v.ArrayOf(
            v.Lazy(get_comment_recur)
        )),
        into=Comment
    )

    assert generate_schema("Comment", comment_validator) == {
        "Comment": {
            'additionalProperties': False,
            'properties': {'name': {'type': 'string',
                                    'pattern': r'^(?!\s*$).+'},
                           'replies': {
                               "type": "array",
                               "items": {"$ref": "#/components/schemas/Comment"}}},
            'required': ['name', 'replies'],
            'type': 'object'
        }
    }


def test_person() -> None:
    @dataclass
    class Person:
        name: str
        email: str
        occupation: str
        country_code: str
        honorifics: List[str]

    person_validator = v.Obj5(
        v.key("name", v.String(v.not_blank)),
        v.key("email", v.String(v.Email(),
                                v.MaxLength(50))),
        v.key("occupation", v.String(v.Enum({"teacher",
                                             "engineer",
                                             "musician",
                                             "cook"}))),
        v.key("country_code", v.String(v.MinLength(2),
                                       v.MaxLength(3))),
        v.key("honorifics",
              v.ArrayOf(
                  v.String(
                      v.RegexValidator(
                          re.compile(r"[A-Z][a-z]+\.]"))),
                  v.unique_items,
                  v.MaxItems(3),
              )
              ),
        into=Person
    )

    assert generate_schema("Person", person_validator) == \
           {"Person": {
               'type': 'object',
               'additionalProperties': False,
               'required': ['name',
                            'email',
                            'occupation',
                            'country_code',
                            'honorifics'],
               'properties':
                   {'name': {
                       'type': 'string',
                       'pattern': r'^(?!\s*$).+'},
                       'email':
                           {'type': 'string',
                            'format': 'email',
                            'maxLength': 50},
                       'occupation':
                           {'type': 'string',
                            'enum': ['cook',
                                     'engineer',
                                     'musician',
                                     'teacher']},
                       'country_code':
                           {'type': 'string',
                            'minLength': 2,
                            'maxLength': 3},
                       'honorifics':
                           {'uniqueItems': True,
                            'type': 'array',
                            'maxItems': 3,
                            'items':
                                {'type': 'string',
                                 'pattern': '[A-Z][a-z]+\\.]'}}}}}


def test_cities() -> None:
    @dataclass
    class CityInfo:
        population: Maybe[int]
        state: str

    state_choices: Set[str] = {"CA", "NY"}

    validate_cities = v.MapOf(
        v.String(),
        v.Obj2(
            v.key("population", v.Nullable(v.Integer(v.Minimum(0)))),
            v.key("state", v.String(v.Enum(state_choices))),
            into=CityInfo
        ),
        v.MaxProperties(3),
        v.MinProperties(2)
    )

    # sanity check
    assert validate_cities(
        {"Oakland": {"population": 450000,
                     "state": "CA"},
         "San Francisco": {"population": None,
                           "state": "CA"}}
    ) == Success({
        "Oakland": CityInfo(Just(450000), "CA"),
        "San Francisco": CityInfo(Nothing, "CA")
    })

    assert generate_schema("City", validate_cities) == {
        "City": {
            "type": "object",
            "additionalProperties": {
                "additionalProperties": False,
                "type": "object",
                "required": ["population", "state"],
                "properties": {
                    "population": {"type": "integer",
                                   "minimum": 0,
                                   "exclusiveMinimum": False,
                                   "nullable": True},
                    "state": {"type": "string",
                              "enum": ["CA", "NY"]}
                },
            },
            "maxProperties": 3,
            "minProperties": 2
        }
    }


def test_auth_creds() -> None:
    @dataclass
    class UsernameCreds:
        username: str
        password: str

    @dataclass
    class EmailCreds:
        email: str
        password: str

    username_creds_validator = v.Obj2(
        v.key("username", v.String(v.not_blank)),
        v.key("password", v.String(v.not_blank)),
        into=UsernameCreds
    )

    email_creds_validator = v.Obj2(
        v.key("email", v.String(v.Email())),
        v.key("password", v.String(v.not_blank)),
        into=EmailCreds
    )

    validator_one_of_2 = v.OneOf2(
        username_creds_validator,
        email_creds_validator
    )

    # sanity check
    assert validator_one_of_2({"username": "a", "password": "b"}) == \
           Success(First(UsernameCreds("a", "b")))

    assert validator_one_of_2({"email": "a@example.com", "password": "b"}) == \
           Success(Second(EmailCreds("a@example.com", "b")))

    assert generate_schema("AuthCreds", validator_one_of_2) == {
        "AuthCreds": {
            "oneOf": [
                {"type": "object",
                 "additionalProperties": False,
                 "required": ["username", "password"],
                 "properties": {
                     "username": {
                         "type": "string",
                         "pattern": r"^(?!\s*$).+"
                     },
                     "password": {
                         "type": "string",
                         "pattern": r"^(?!\s*$).+"
                     }
                 }},
                {"type": "object",
                 "additionalProperties": False,
                 "required": ["email", "password"],
                 "properties": {
                     "email": {
                         "type": "string",
                         "format": "email"
                     },
                     "password": {
                         "type": "string",
                         "pattern": r"^(?!\s*$).+"
                     }
                 }}
            ]
        }
    }

    @dataclass
    class Token:
        token: str

    validator_one_of_3 = v.OneOf3(
        username_creds_validator,
        email_creds_validator,
        v.Obj1(v.key("token", v.String(v.MinLength(32),
                                       v.MaxLength(32))),
               into=Token)
    )

    # sanity
    assert validator_one_of_3({"token": "abcdefghijklmnopqrstuvwxyz123456"}) == \
           Success(Third(Token("abcdefghijklmnopqrstuvwxyz123456")))

    assert generate_schema("AuthCreds", validator_one_of_3) == {
        "AuthCreds": {
            "oneOf": [
                {"type": "object",
                 "additionalProperties": False,
                 "required": ["username", "password"],
                 "properties": {
                     "username": {
                         "type": "string",
                         "pattern": r"^(?!\s*$).+"
                     },
                     "password": {
                         "type": "string",
                         "pattern": r"^(?!\s*$).+"
                     }
                 }},
                {"type": "object",
                 "additionalProperties": False,
                 "required": ["email", "password"],
                 "properties": {
                     "email": {
                         "type": "string",
                         "format": "email"
                     },
                     "password": {
                         "type": "string",
                         "pattern": r"^(?!\s*$).+"
                     }
                 }},
                {"type": "object",
                 "additionalProperties": False,
                 "required": ["token"],
                 "properties": {
                     "token": {
                         "type": "string",
                         "minLength": 32,
                         "maxLength": 32
                     }
                 }}
            ]
        }
    }


def test_forecast() -> None:
    validator = v.MapOf(
        v.Date(),
        v.Float()
    )

    # sanity
    assert validator({
        "2021-04-06": 55.5,
        "2021-04-07": 57.9
    }) == Success({date(2021, 4, 6): 55.5,
                   date(2021, 4, 7): 57.9})

    assert generate_schema("Forecast", validator) == {
        "Forecast": {
            "type": "object",
            "additionalProperties": {
                "type": "number"
            }
        }
    }


def test_tuples() -> None:
    validator = v.Tuple2(
        v.String(v.not_blank),
        v.Tuple3(
            v.String(),
            v.Integer(),
            v.Boolean()
        )
    )

    # sanity check
    assert validator(["ok", ["", 0, False]]) == Success(
        ("ok", ("", 0, False))
    )

    assert generate_schema("Tuples", validator) == {
        "Tuples": {
            "description": 'a 2-tuple; schemas for slots are '
                           'listed in order in "items" > "anyOf"',
            "type": "array",
            "maxItems": 2,
            "items": {
                "anyOf": [
                    {"type": "string",
                     "pattern": r"^(?!\s*$).+"},
                    {
                        "description": 'a 3-tuple; schemas for slots are '
                                       'listed in order in "items" > "anyOf"',
                        "type": "array",
                        "maxItems": 3,
                        "items": {
                            "anyOf": [
                                {"type": "string"},
                                {"type": "integer"},
                                {"type": "boolean"}
                            ]
                        }
                    }
                ]
            }
        }
    }
