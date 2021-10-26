from typing import TypeVar, Callable

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")
G = TypeVar("G")
H = TypeVar("H")
I = TypeVar("I")

Ret = TypeVar('Ret')

Fn0 = Callable[[], Ret]
Fn1 = Callable[[A], Ret]
Fn2 = Callable[[A, B], Ret]
Fn3 = Callable[[A, B, C], Ret]
Fn4 = Callable[[A, B, C, D], Ret]
Fn5 = Callable[[A, B, C, D, E], Ret]
Fn6 = Callable[[A, B, C, D, E, F], Ret]
Fn7 = Callable[[A, B, C, D, E, F, G], Ret]
Fn8 = Callable[[A, B, C, D, E, F, G, H], Ret]
Fn9 = Callable[[A, B, C, D, E, F, G, H, I], Ret]
