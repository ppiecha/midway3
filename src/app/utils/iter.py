from collections.abc import Callable, Iterable
from functools import reduce


def replace_all(fn: Callable, it: Iterable) -> Iterable:
    return tuple([replace_all(fn, i) if isinstance(i, Iterable) else fn(i) for i in it])

def compose(*funcs):
    return lambda x: reduce(lambda f, g: g(f), list(funcs), x)