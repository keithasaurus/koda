from koda import Just, Maybe, nothing


def str_to_int(a: str) -> Maybe[int]:
    try:
        int_val = int(a)
    except ValueError:
        return nothing
    else:
        return Just(int_val)


x = str_to_int("5").map(str).get_or_else("ok")
