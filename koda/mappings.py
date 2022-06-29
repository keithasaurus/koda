from typing import Mapping

from koda._generics import A, B
from koda.maybe import Maybe, just, nothing


def mapping_get(data: Mapping[A, B], key: A) -> Maybe[B]:
    # this is better than data.get(...) because if None is a valid return value,
    # there's no way to know if the value is the value from the map or the deafult value
    try:
        return just(data[key])
    except KeyError:
        return nothing
