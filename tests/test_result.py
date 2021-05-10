import math

from koda.result import Err, Result, Ok
from koda.utils.test import (
    enforce_applicative_apply,
    enforce_functor_one_val,
    enforce_monad_flat_map,
    enforce_monad_unit,
)
from koda.validation import chain


def test_result() -> None:
    enforce_functor_one_val(Ok, "map")
    enforce_monad_unit(Ok)
    enforce_monad_flat_map(Ok, Err("something went wrong"))
    enforce_applicative_apply(Ok, Err("something went wrong"))


def _string_to_int(s: str) -> Result[int, str]:
    try:
        return Ok(int(s))
    except ValueError:
        return Err("could not convert string to int")


def _safe_square_root(n: int) -> Result[float, str]:
    try:
        return Ok(math.sqrt(n))
    except ValueError:
        return Err("input not valid for square root")


def test_chain2() -> None:
    chained = chain(_string_to_int, _safe_square_root)

    assert Ok(5.0) == _string_to_int("25").flat_map(_safe_square_root) == chained("25")

    assert (
        Err("could not convert string to int")
        == _string_to_int("asdas").flat_map(_safe_square_root)
        == chained("asdas")
    )

    assert (
        Err("input not valid for square root")
        == _string_to_int("-5").flat_map(_safe_square_root)
        == chained("-5")
    )


def _max_4(f: float) -> Result[float, str]:
    if f > 4.0:
        return Err("value above 4.0")
    else:
        return Ok(f)


def test_chain3() -> None:
    chained = chain(_string_to_int, _safe_square_root, _max_4)

    assert (
        Ok(3.0)
        == _string_to_int("9").flat_map(_safe_square_root).flat_map(_max_4)
        == chained("9")
    )

    assert (
        Err("value above 4.0")
        == _string_to_int("25").flat_map(_safe_square_root).flat_map(_max_4)
        == chained("25")
    )

    assert (
        Err("could not convert string to int")
        == _string_to_int("asdas").flat_map(_safe_square_root).flat_map(_max_4)
        == chained("asdas")
    )

    assert (
        Err("input not valid for square root")
        == _string_to_int("-5").flat_map(_safe_square_root)
        == chained("-5")
    )


def _min_2_chars(s: str) -> Result[str, str]:
    if len(s) < 2:
        return Err("must be two characters or greater")
    else:
        return Ok(s)


def test_chain4() -> None:
    chained = chain(_min_2_chars, _string_to_int, _safe_square_root, _max_4)

    assert (
        Err("must be two characters or greater")
        == (
            _min_2_chars("9")
            .flat_map(_string_to_int)
            .flat_map(_safe_square_root)
            .flat_map(_max_4)
        )
        == chained("9")
    )

    assert (
        Err("value above 4.0")
        == (
            _min_2_chars("25")
            .flat_map(_string_to_int)
            .flat_map(_safe_square_root)
            .flat_map(_max_4)
        )
        == chained("25")
    )

    assert (
        Err("could not convert string to int")
        == (
            _min_2_chars("asdas")
            .flat_map(_string_to_int)
            .flat_map(_safe_square_root)
            .flat_map(_max_4)
        )
        == chained("asdas")
    )

    assert (
        Err("input not valid for square root")
        == (_min_2_chars("-25").flat_map(_string_to_int).flat_map(_safe_square_root))
        == chained("-5")
    )
