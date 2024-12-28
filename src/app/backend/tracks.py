from collections.abc import Iterator
from functools import wraps
from typing import Iterable

from src.app.backend.types import (
    DEFAULT_VELOCITY,
    Notes,
    Event,
    TrackArgs,
    MidiEvent,
    EventKind,
    DEFAULT,
)
from src.app.utils.iter import replace_all, peek
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def events_fn(notes: Notes) -> Iterator[Event]:
    if not notes or not notes.keys:
        return
    if not notes.velocities:
        notes = notes._replace(velocities=replace_all(lambda x: DEFAULT_VELOCITY, notes.keys))
    if not notes.programs:
        notes = notes._replace(programs=replace_all(lambda x: None, notes.keys))
    if not notes.controls:
        notes = notes._replace(controls=replace_all(lambda x: None, notes.keys))
    # logger.debug(f"{notes = }")
    for note in zip(*notes):
        yield Event(*note)


def args_wrapper(tick, channel, program_, u2t):
    def midi_events_from_events(events: Iterator[Event]) -> Iterator[MidiEvent]:
        res = peek(iterator=events)
        if not res:
            return
        _, events = res
        nonlocal tick
        yield MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program_, None)
        for time, key, duration, velocity, program, control in events:
            yield MidiEvent(EventKind.NOTE, tick, channel, key, u2t(duration), velocity, program, control)
            if program:
                yield MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program, None)
            if control:
                yield MidiEvent(EventKind.CONTROL, tick, channel, None, None, None, None, control)
            tick += u2t(time)
            midi_events_from_events.tick = tick

    return midi_events_from_events


# TODO change from function to class with methods
def track_wrapper():
    tracks = {}

    def track_outer(channel: str, soundfont: str = DEFAULT, bank: int = 0, preset: int = 0):
        def decorator(fn):
            tracks[fn.__name__] = TrackArgs(
                name=fn.__name__, channel_name=channel, notes=fn, soundfont=soundfont, bank=bank, preset=preset
            )

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
