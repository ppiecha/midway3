from typing import NamedTuple

type Key = int


class Key(NamedTuple):
    value: int


t: Key = 1
k = Key(value=1)

d = globals().copy()
for k, v in d.items():
    print(k, v)
