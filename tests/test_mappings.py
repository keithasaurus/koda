from typing import Optional

from koda import just, nothing
from koda.mappings import mapping_get


def test_mapping_get() -> None:
    d: dict[str, Optional[str]] = {"a": None, "b": "ok"}

    assert mapping_get(d, "a") == just(None)
    assert mapping_get(d, "b") == just("ok")
    assert mapping_get(d, "c") == nothing
