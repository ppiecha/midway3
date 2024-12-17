from functools import wraps
from typing import NamedTuple, Iterable, Callable

from src.app.backend.types import DEFAULT_VELOCITY, Notes, Event
from src.app.utils.iter import replace_all
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def events(notes: Notes) -> Iterable[Event]:
    if notes.velocities is None:
        notes._replace(velocities=replace_all(lambda x: DEFAULT_VELOCITY, notes.keys))
    return tuple(Event(*e) for e in zip(*notes))


class TrackArgs(NamedTuple):
    name: str
    channel: str
    font: str
    notes: Callable
    bank: int = 0
    preset: int = 0


def track_wrapper():
    tracks = {}

    def track_outer(channel: str, font: str, bank: int = 0, preset: int = 0):
        def decorator(fn):
            tracks[fn.__name__] = TrackArgs(fn.__name__, channel, font, fn, bank, preset)

            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)

            return inner

        return decorator

    def channels_decorator(fn):
        track_outer.channels_map_func = fn

        @wraps(fn)
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)

        return inner

    def soundfonts_decorator(fn):
        track_outer.soundfonts_map_func = fn

        @wraps(fn)
        def inner(*args, **kwargs):
            return fn(*args, **kwargs)

        return inner

    track_outer.tracks = tracks
    track_outer.channels = channels_decorator
    track_outer.soundfonts = soundfonts_decorator

    return track_outer


track = track_wrapper()
