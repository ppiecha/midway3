import itertools


def gen1():
    for i in range(10):
        yield i


g = gen1()

h = itertools.accumulate(g, lambda x, y: x + y, initial=0)
print(type(h))
print(list(h))
