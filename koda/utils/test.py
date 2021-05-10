from typing import Any, Type, TypeVar

from koda import compose, identity

A = TypeVar("A")

__all__ = (
    "enforce_functor_one_val",
    "enforce_monad_unit",
    "enforce_monad_flat_map",
    "enforce_applicative_apply",
)


def _int_inc_5(x: int) -> int:
    return x + 5


def _int_to_str(x: int) -> str:
    return str(x)


def enforce_functor_one_val(functorable: Type[Any], map_method: str) -> None:
    """
    requiring map_method to be specified, because the mapping may
    be done by variously named methods
    """
    test_val: int = 10
    obj = functorable(test_val)

    # map id should return same val
    assert getattr(obj, map_method)(identity) == functorable(test_val)

    # map should work
    assert getattr(obj, map_method)(_int_inc_5) == functorable(test_val + 5)

    # should be associative
    two_maps_val1 = getattr(obj, map_method)(_int_inc_5)
    two_maps_val2 = getattr(two_maps_val1, map_method)(_int_to_str)
    composed_val = getattr(obj, map_method)(compose(_int_inc_5, _int_to_str))

    assert two_maps_val2 == composed_val


def enforce_monad_unit(unitable: Type[Any]) -> None:
    test_val: int = 10
    assert unitable(test_val).val == test_val


def enforce_monad_flat_map(bindable: Type[Any], non_bindable: Any) -> None:
    # should be able to flatmap left
    test_val: int = 10

    def flat_mapped(x: int) -> Any:
        return bindable(_int_inc_5(x))

    assert bindable(test_val).flat_map(flat_mapped) == bindable(test_val + 5)

    assert bindable(test_val).flat_map(lambda _: non_bindable) == non_bindable

    assert non_bindable.flat_map(_int_inc_5) == non_bindable


def enforce_applicative_apply(applyable: Type[Any], non_applyable: Any) -> None:
    test_val: int = 10
    assert applyable(test_val).apply(applyable(_int_to_str)) == applyable(
        _int_to_str(test_val)
    )

    assert applyable(test_val).apply(non_applyable) == non_applyable

    assert non_applyable.apply(applyable(_int_to_str)) == non_applyable
