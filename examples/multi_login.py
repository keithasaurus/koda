from typing import NamedTuple

from koda.either import Either
from koda.json.validation import (Email, NotBlank, Obj2, OneOf2, String, prop,
                                  unwrap_jsonable)
from koda.result import Err


class UsernameAuthCreds(NamedTuple):
    username: Either[str, str]
    password: str


username_validator = Obj2(
    prop("username", OneOf2(
        ("username", String(Email())),
        ("email", String(NotBlank())),
    )),
    prop("password", String(NotBlank())),
    into=UsernameAuthCreds
)

result = username_validator(
    {"password": "",
     "username": " "}
)

if isinstance(result, Err):
    print(unwrap_jsonable(result.val))
else:
    print(result)
