from dataclasses import dataclass

from koda.conversions import maybe_to_result, result_to_maybe, to_maybe
from koda.maybe import just, nothing
from koda.result import err, ok


def test_to_maybe() -> None:
    assert to_maybe(5) == just(5)
    assert to_maybe("abc") == just("abc")
    assert to_maybe(False) == just(False)

    assert to_maybe(None) == nothing


def test_maybe_to_result() -> None:
    @dataclass
    class SomeError:
        msg: str
        params: list[str]

    fail_message = SomeError("it failed", ["a", "b"])

    assert maybe_to_result(fail_message, just(5)) == ok(5)

    assert maybe_to_result(fail_message, nothing) == err(fail_message)


def test_result_to_maybe() -> None:
    assert result_to_maybe(ok(3)) == just(3)
    assert result_to_maybe(err("something")) == nothing
