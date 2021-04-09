from typing import NamedTuple

from koda.either import Either
from koda.json.validation import (Email, NotBlank, Obj2, OneOf2, String, key,
                                  unwrap_jsonable)
from koda.result import Failure


class UsernameAuthCreds(NamedTuple):
    username: Either[str, str]
    password: str


username_validator = Obj2(
    key("username", OneOf2(
        ("username", String(Email())),
        ("email", String(NotBlank())),
    )),
    key("password", String(NotBlank())),
    into=UsernameAuthCreds
)

result = username_validator(
    {"password": "",
     "username": " "}
)

if isinstance(result, Failure):
    print(unwrap_jsonable(result.val))
else:
    print(result)
