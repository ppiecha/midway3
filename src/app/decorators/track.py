from functools import wraps
from typing import NamedTuple

from src.app.backend.types import (
    DEFAULT_VELOCITY,
    Notes,
    Event,
    TrackArgs,
    DEFAULT,
    TrackRegistry,
    SoundfontsMapFunc,
    ChannelsMapFunc,
    Gen,
)
from src.app.utils.iter import replace_all
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def events_fn(notes: Notes) -> Gen[Event]:
    if not notes or not notes.keys:
        return
    if not notes.velocities:
        notes = notes._replace(velocities=replace_all(lambda x: DEFAULT_VELOCITY, notes.keys))
    if not notes.programs:
        notes = notes._replace(programs=replace_all(lambda x: None, notes.keys))
    if not notes.controls:
        notes = notes._replace(controls=replace_all(lambda x: None, notes.keys))
    for note in zip(*notes):
        yield Event(*note)


class Track(NamedTuple):

    registry: TrackRegistry = {}
    mappings = {}

    def __call__(self, channel: str, soundfont: str = DEFAULT, bank: int = 0, preset: int = 0):
        def decorator(fn):
            self.registry[fn.__name__] = TrackArgs(
                name=fn.__name__, channel_name=channel, notes_fn=fn, soundfont=soundfont, bank=bank, preset=preset
            )

            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)

            return inner

        return decorator

    @property
    def channels_map_func(self):
        return self.mappings["channels_map_func"]

    def channels(self, fn: ChannelsMapFunc):
        self.mappings["channels_map_func"] = fn

        @wraps(fn)
        def inner():
            return fn()

        return inner

    @property
    def soundfonts_map_func(self):
        return self.mappings["soundfonts_map_func"]

    def soundfonts(self, fn: SoundfontsMapFunc):
        self.mappings["soundfonts_map_func"] = fn

        @wraps(fn)
        def inner():
            return fn()

        return inner


track = Track()
