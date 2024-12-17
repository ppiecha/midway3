from collections.abc import Callable, Iterable


def replace_all(fn: Callable, it: Iterable) -> Iterable:
    return tuple([replace_all(fn, i) if isinstance(i, Iterable) else fn(i) for i in it])
