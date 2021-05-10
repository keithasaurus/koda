from decimal import Decimal
from typing import List, Tuple

from koda.tuple import ntuple, typed_tuple


def test_ntuple() -> None:
    assert ntuple(1, 2, 3) == (1, 2, 3)


def test_typed_tuple() -> None:
    t1: Tuple[int] = typed_tuple(5)
    assert t1 == (5,)

    t2: Tuple[int, str] = typed_tuple(5, "ok")
    assert t2 == (5, "ok")

    t3: Tuple[float, None, str] = typed_tuple(5.5, None, "something")
    assert t3 == (5.5, None, "something")

    t4: Tuple[int, int, Decimal, bool] = typed_tuple(5, 10, Decimal("15.0"), False)
    assert t4 == (5, 10, Decimal("15.0"), False)

    t5: Tuple[int, int, Decimal, bool, List[str]] = typed_tuple(
        5, 10, Decimal("15.0"), False, ["a", "bc"]
    )
    assert t5 == (5, 10, Decimal("15.0"), False, ["a", "bc"])

    t6: Tuple[int, int, Decimal, bool, List[str], None] = typed_tuple(
        5, 10, Decimal("15.0"), False, ["a", "bc"], None
    )
    assert t6 == (5, 10, Decimal("15.0"), False, ["a", "bc"], None)

    t7: Tuple[int, int, Decimal, bool, List[str], None, int] = typed_tuple(
        5, 10, Decimal("15.0"), False, ["a", "bc"], None, -1
    )
    assert t7 == (5, 10, Decimal("15.0"), False, ["a", "bc"], None, -1)

    t8: Tuple[int, int, Decimal, bool, List[str], None, int, int] = typed_tuple(
        5, 10, Decimal("15.0"), False, ["a", "bc"], None, -1, 0
    )
    assert t8 == (5, 10, Decimal("15.0"), False, ["a", "bc"], None, -1, 0)
