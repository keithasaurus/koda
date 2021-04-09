from typing import Hashable, NamedTuple, TypeVar

from koda.json.validation import Email, MaxLength, Obj5, String, maybe_prop, prop
from koda.maybe import Maybe

KeyT = TypeVar('KeyT', bound=Hashable)


class ContactMessageAPI(NamedTuple):
    name: str
    email: str
    subject: Maybe[str]
    message: str
    body: str


validate_message = Obj5(
    prop("name", String(MaxLength(100))),
    prop("email", String(MaxLength(100),
                         Email())),
    maybe_prop("subject", String(MaxLength(100))),
    prop("message", String()),
    prop("body", String()),
    into=ContactMessageAPI,
)

print(
    validate_message({"name": "keith",
                      "subject": "some site email",
                      "message": "hi, this is the message i've made for you",
                      "email": "keith@something.com",
                      "body": "something"})
)
