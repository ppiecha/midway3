from functools import wraps
from typing import Iterable

from src.app.backend.types import (
    DEFAULT_VELOCITY,
    Notes,
    Event,
    TrackArgs,
    MusicArgs,
    Channels,
    UnitToTick,
    MidiEvent,
    Tick,
    EventKind,
)
from src.app.utils.iter import replace_all
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def events_fn(notes: Notes) -> Iterable[Event]:
    if not notes.velocities:
        notes = notes._replace(velocities=replace_all(lambda x: DEFAULT_VELOCITY, notes.keys))
    if not notes.programs:
        notes = notes._replace(programs=replace_all(lambda x: None, notes.keys))
    if not notes.controls:
        notes = notes._replace(controls=replace_all(lambda x: None, notes.keys))
    logger.debug(f"{notes = }")
    for note in zip(*notes):
        yield Event(*note)

def args_wrapper(tick, channel, program_, u2t):
    def midi_events_from_events(events: Iterable[Event]) -> Iterable[MidiEvent]:
        nonlocal tick
        yield MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program_, None)
        for time, key, duration, velocity, program, control in events:
            yield MidiEvent(EventKind.NOTE, tick, channel, key, u2t(duration), velocity, program, control)
            if program:
                yield MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program, None)
            if control:
                yield MidiEvent(EventKind.CONTROL, tick, channel, None, None, None, None, control)
            tick += u2t(time)
    return midi_events_from_events

def track_wrapper():
    tracks = {}

    def track_outer(channel: str, bank: int = 0, preset: int = 0):
        def decorator(fn):
            tracks[fn.__name__] = TrackArgs(fn.__name__, channel, fn, bank, preset)

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

    track_outer.tracks = tracks
    track_outer.channels = channels_decorator

    return track_outer


track = track_wrapper()
