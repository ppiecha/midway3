from typing import Iterable

lst = [[1, 2], 3, [4]]
# b = [100 for a in lst for b in a]

print(isinstance(1, Iterable))


def replace_all(fn, it: Iterable) -> Iterable:
    return tuple([replace_all(fn, i) if isinstance(i, Iterable) else fn(i) for i in it])


print(replace_all(lambda x: x, lst))
print(list(map(lambda x: 5, lst)))
