from typing import NamedTuple, Iterable, Set


class Notes(NamedTuple):
    times: Iterable[float]
    keys: Iterable[int|None|Set[int]]

notes = Notes(
    times=(1,2,3,4),
    keys=(0, 0, 0, 0)
)

print(isinstance(notes, Iterable))

print(list(zip(notes.times, notes.keys)))
print(list(zip(*notes)))

print(type(()))

