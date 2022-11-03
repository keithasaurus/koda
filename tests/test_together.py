from koda import Err, Fifth, First, Fourth, Just, Ok, Second, Third, nothing


def test_equivalence() -> None:
    assert Ok(5) == Ok(5)
    assert Ok(5) != Ok(4)
    # obey default python equivalence for inner values
    assert Ok(5.0) == Ok(5)
    assert Ok(5) != Just(5)
    assert Ok(5) != 5

    assert Err(5) == Err(5)
    assert Err(5) != Err(4)
    # obey default python equivalence for inner values
    assert Err(5.0) == Err(5)
    assert Err(5) != Just(5)
    assert Err(5) != 5

    assert Just(5) == Just(5)
    assert Just(5) != Just(4)
    # obey default python equivalence for inner values
    assert Just(5.0) == Just(5)
    assert Just(5) != Ok(5)
    assert Just(5) != 5

    assert First(5) == First(5)
    assert First(5) != First(4)
    # obey default python equivalence for inner values
    assert First(5.0) == First(5)
    assert First(5) != Ok(5)
    assert First(5) != 5

    assert Second(5) == Second(5)
    assert Second(5) != Second(4)
    # obey default python equivalence for inner values
    assert Second(5.0) == Second(5)
    assert Second(5) != Ok(5)
    assert Second(5) != 5

    assert Third(5) == Third(5)
    assert Third(5) != Third(4)
    # obey default python equivalence for inner values
    assert Third(5.0) == Third(5)
    assert Third(5) != Ok(5)
    assert Third(5) != 5

    assert Fourth(5) == Fourth(5)
    assert Fourth(5) != Fourth(4)
    # obey default python equivalence for inner values
    assert Fourth(5.0) == Fourth(5)
    assert Fourth(5) != Ok(5)
    assert Fourth(5) != 5

    assert Fifth(5) == Fifth(5)
    assert Fifth(5) != Fifth(4)
    # obey default python equivalence for inner values
    assert Fifth(5.0) == Fifth(5)
    assert Fifth(5) != Ok(5)
    assert Fifth(5) != 5


def test_repr() -> None:
    for obj, expected in [
        (Ok(5), "Ok(5)"),
        (Err(5), "Err(5)"),
        (Just("123"), "Just('123')"),
        (nothing, "Nothing()"),
        (First(1), "First(1)"),
        (Second(1), "Second(1)"),
        (Third(1), "Third(1)"),
        (Fourth(1), "Fourth(1)"),
        (Fifth(1), "Fifth(1)"),
    ]:
        assert repr(obj) == expected
