from functools import wraps
from typing import NamedTuple, Callable


class PlayerArgs(NamedTuple):
    bpm: int
    soundfont_path: str
    ticks_per_beat: int
    sequence: Callable

def player_wrapper():
    args = None
    def outer(bpm: int, soundfont_path: str, ticks_per_beat: int = 96):
        def decorator(fn):
            nonlocal args
            args = PlayerArgs(bpm, soundfont_path, ticks_per_beat, fn)
            @wraps(fn)
            def inner(*args_, **kwargs):
                return fn(*args_, **kwargs)
            return inner
        return decorator
    outer.args = args
    return outer

player = player_wrapper()
