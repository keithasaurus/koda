from koda import Err, Fifth, First, Fourth, Just, Nothing, Ok, Second, Third, nothing


def test_match_works_as_expected() -> None:
    """
    just making sure we have __match_args__ set.
    """
    match Ok(5):
        case Ok(num):
            assert num == 5
        case _:
            assert False, "shouldn't have gotten here!"

    match Err(6):
        case Err(num):
            assert num == 6
        case _:
            assert False, "shouldn't have gotten here!"

    match Just(7):
        case Just(num):
            assert num == 7
        case _:
            assert False, "shouldn't have gotten here!"

    match nothing:
        case Nothing():
            assert True
        case _:
            assert False, "shouldn't have gotten here!"

    match First(1):
        case First(num):
            assert num == 1
        case _:
            assert False, "shouldn't have gotten here!"

    match Second(5):
        case Second(num):
            assert num == 5
        case _:
            assert False, "shouldn't have gotten here!"

    match Third(5):
        case Third(num):
            assert num == 5
        case _:
            assert False, "shouldn't have gotten here!"

    match Fourth(5):
        case Fourth(num):
            assert num == 5
        case _:
            assert False, "shouldn't have gotten here!"

    match Fifth(5):
        case Fifth(num):
            assert num == 5
        case _:
            assert False, "shouldn't have gotten here!"


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
