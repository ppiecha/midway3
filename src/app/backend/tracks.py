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
    return tuple(Event(*e) for e in zip(*notes))


def track_midi_events_fn(
    music_args: MusicArgs, track_args: TrackArgs, u2t: UnitToTick, tick: Tick
) -> tuple[Tick, set[MidiEvent]]:
    midi_events: set[MidiEvent] = set()
    track = music_args.track
    channels: Channels = track.channels_map_func()
    notes = track_args.notes()
    events = events_fn(notes=notes)
    channel = channels[track_args.channel_name]
    for time, key, duration, velocity, program, control in events:
        midi_events.add(MidiEvent(EventKind.NOTE, tick, channel, key, u2t(duration), velocity, program, control))
        if program:
            midi_events.add(MidiEvent(EventKind.PROGRAM, tick, channel, key, 0, velocity, program, control))
        if control:
            midi_events.add(MidiEvent(EventKind.CONTROL, tick, channel, key, 0, velocity, program, control))
        tick += u2t(time)
    return tick, midi_events


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
