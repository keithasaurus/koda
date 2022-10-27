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
