from collections import defaultdict
from functools import wraps
from typing import NamedTuple, Iterable, Set, Callable


class Notes(NamedTuple):
    times: Iterable[float]
    keys: Iterable[int|None|Set[int]]
    durations: Iterable[float|Set[int]]
    velocities: Iterable[int|Set[int]] #|None = None

class TrackArgs(NamedTuple):
    name: str
    channel: str
    font: str
    notes: Callable
    bank: int = 0
    preset: int = 0

def track_wrapper():
    tracks = defaultdict(list)
    def outer(channel: str, font: str, bank: int = 0, preset: int = 0):
        def decorator(fn):
            tracks[fn.__name__].append(TrackArgs(fn.__name__, channel, font, fn, bank, preset))
            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)
            return inner
        return decorator

    def channels_decorator(fn):
        outer.channels_map_func = fn
        @wraps(fn)
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)
        return inner

    outer.tracks = tracks
    outer.channels = channels_decorator
    return outer

track = track_wrapper()