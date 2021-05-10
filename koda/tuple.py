from typing import Tuple, TypeVar

from koda._cruft.tuple import _typed_tuple

A = TypeVar("A")

__all__ = ("typed_tuple", "ntuple")

typed_tuple = _typed_tuple


def ntuple(*vals: A) -> Tuple[A, ...]:
    """
    takes *vals of the same type and returns a tuple of that type
    useful for the casting of the type.
    """
    return vals
