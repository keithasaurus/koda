from typing import TypeVar, Generic, Union, Callable, Any, List

from koda import load_once, thunkify
from koda.maybe import Nothing, Maybe, Just

A = TypeVar('A')
B = TypeVar('B')


class EmptyType:
    def drop(self, n: int) -> "EmptyType":
        return self

    def fold_right(self, fn: Callable[[B, Any], B], accum: B) -> B:
        return accum

    def

    def take(self, n: int) -> "EmptyType":
        return self

    def head(self) -> Maybe[Any]:
        return Nothing


Empty = EmptyType()


class Cons(Generic[A]):
    def __init__(self,
                 val: Callable[[], A],
                 tail: Callable[[], "LazyList[A]"]) -> None:
        # never re-evaluate
        self.val = load_once(val)
        self.tail = load_once(tail)

    def drop(self, n: int) -> "LazyList[A]":
        if n <= 0:
            return self
        else:
            return self.tail().drop(n - 1)

    def fold_right(self,
                   fn: Callable[[B, A], B],
                   accum: B) -> B:
        return fn(self.tail().fold_right(fn, accum),
                  self.val())

    def head(self) -> Maybe[A]:
        return Just(self.val())

    def take(self, n: int) -> "LazyList[A]":
        if n <= 0:
            return Empty
        else:
            return Cons(self.val, thunkify(self.tail().take(n - 1)))

    def __repr__(self) -> str:
        s: List[str] = []
        curr: "LazyList[A]" = self
        while True:
            if isinstance(curr, EmptyType):
                break
            else:
                s.append(curr.val().__repr__())
                curr = curr.tail()
        joined = ", ".join(s)
        return f"LazyList({joined})"


LazyList = Union[EmptyType, Cons[A]]


def lazy_list(*objs: A) -> LazyList[A]:
    """
    helper to allow simple init

    >>> lazy_list(1, 2, 3)
    LazyList(1, 2, 3)

    >>> lazy_list()
    LazyList()
    """
    if len(objs) == 0:
        return Empty
    else:
        ll: LazyList[A] = Empty

        # avoiding recursion
        for obj in objs[::-1]:
            ll = Cons(thunkify(obj), thunkify(ll))
        return ll


if __name__ == '__main__':
    print(
        lazy_list(1, 2, 3, 2, 5).drop(2).take(2)
    )
