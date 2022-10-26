from argparse import ArgumentParser
from time import perf_counter
from typing import Callable

from koda import Err, Just, Nothing, Ok


def create_ok(iterations: int) -> None:
    for i in range(iterations):
        Ok(i)


def create_err(iterations: int) -> None:
    for i in range(iterations):
        Err(i)


def create_just(iterations: int) -> None:
    for i in range(iterations):
        Just(i)


def create_nothing(iterations: int) -> None:
    for i in range(iterations):
        Nothing()


benches: dict[str, Callable[[int], None]] = {
    "create_ok": create_ok,
    "create_err": create_err,
    "create_just": create_just,
    "create_nothing": create_nothing,
}


def run_bench(iterations: int, fn: Callable[[int], None]) -> None:
    start = perf_counter()
    fn(iterations)
    t_ = perf_counter() - start
    print(f"Execution time: {t_:.4f} secs\n")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "tests",
        type=str,
        nargs="*",
        help="which tests to run",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1_000_000,
        help="How many iterations of each test we'll run",
    )
    args = parser.parse_args()

    print(f"{args.iterations} ITERATIONS")

    for name, fn in benches.items():
        if args.tests == [] or name in args.tests:
            print(f"----- BEGIN {name} -----\n")
            run_bench(args.iterations, fn)
            print(f"----- END {name} -----\n")
