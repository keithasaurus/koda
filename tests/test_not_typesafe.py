"""
This file should be ignored by mypy.

The tests in it are designed to prevent the maintainers of this
repo from breaking userland code if it's used incorrectly. For instance,
we don't want to compile Koda in such a way that it breaks
Ok(5).map(someFuncWithAnInvalidTypeSignature).
"""
from koda import Err, Fifth, First, Fourth, Just, Ok, Second, Third, nothing


def test_can_do_bad_mappings() -> None:
    def example_float_func(f: str) -> str:
        return f

    assert Ok(5).map(example_float_func) == Ok(5)
    assert Err(5).map(example_float_func) == Err(5)
    assert Just(5).map(example_float_func) == Just(5)
    assert nothing.map(example_float_func) is nothing
    assert First(5).map_first(example_float_func) == First(5)
    assert Second(5).map_second(example_float_func) == Second(5)
    assert Third(5).map_third(example_float_func) == Third(5)
    assert Fourth(5).map_fourth(example_float_func) == Fourth(5)
    assert Fifth(5).map_fifth(example_float_func) == Fifth(5)
