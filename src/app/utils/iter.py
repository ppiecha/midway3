import itertools
from collections.abc import Callable, Iterable
from functools import reduce


def replace_all(fn: Callable, it: Iterable) -> Iterable:
    return tuple([replace_all(fn, i) if isinstance(i, Iterable) else fn(i) for i in it])


def compose(*funcs):
    return lambda x: reduce(lambda f, g: g(f), list(funcs), x)


def peek(iterator):
    if not iterator:
        return None
    try:
        first = next(iterator)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterator)
