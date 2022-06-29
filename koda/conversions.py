from typing import Any, Optional

from koda._generics import A, FailT
from koda.maybe import Just, Maybe, just, nothing
from koda.result import Ok, Result, err, ok


def maybe_to_result(fail_message: FailT, orig: Maybe[A]) -> Result[A, FailT]:
    if isinstance(orig.variant, Just):
        return ok(orig.variant.val)
    else:
        return err(fail_message)


def to_maybe(val: Optional[A]) -> Maybe[A]:
    if val is None:
        return nothing
    else:
        return just(val)


def result_to_maybe(orig: Result[A, Any]) -> Maybe[A]:
    return just(orig.variant.val) if isinstance(orig.variant, Ok) else nothing
