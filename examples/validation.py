from typing import Hashable, NamedTuple, TypeVar

from koda.json.validation import Email, MaxLength, Obj5, String, key, maybe_key
from koda.maybe import Maybe

KeyT = TypeVar('KeyT', bound=Hashable)


class ContactMessageAPI(NamedTuple):
    name: str
    email: str
    subject: Maybe[str]
    message: str
    body: str


validate_message = Obj5(
    key("name", String(MaxLength(100))),
    key("email", String(MaxLength(100),
                        Email())),
    maybe_key("subject", String(MaxLength(100))),
    key("message", String()),
    key("body", String()),
    into=ContactMessageAPI,
)

print(
    validate_message({"name": "keith",
                      "subject": "some site email",
                      "message": "hi, this is the message i've made for you",
                      "email": "keith@something.com",
                      "body": "something"})
)
