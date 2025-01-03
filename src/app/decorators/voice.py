import functools
import itertools
from collections.abc import Iterator
from functools import wraps
from typing import Iterable, NamedTuple

from src.app.backend.types import (
    DEFAULT_VELOCITY,
    Notes,
    Event,
    VoiceArgs,
    MidiEvent,
    EventKind,
    DEFAULT,
    VoiceRegistry,
    SoundfontsMapFunc,
    ChannelsMapFunc,
    MidiEventsWithTick,
)
from src.app.utils.iter import replace_all, peek
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def events_fn(notes: Notes) -> Iterable[Event]:
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


# def args_wrapper(tick, channel, program_, u2t):
#     def add_midi_event(events_with_tick: MidiEventsWithTick, event: Event) -> MidiEventsWithTick:
#         return MidiEventsWithTick(
#             tick=events_with_tick.tick.add(event.time),
#             midi_events=itertools.chain(events_with_tick.midi_events, midi_events_from_event(event))
#         )
#
#     def midi_events_from_event(event: Event):
#         time, key, duration, velocity, program, control = event
#         yield MidiEvent(EventKind.NOTE, tick, channel, key, u2t(duration), velocity, program, control)
#         if program:
#             yield MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program, None)
#         if control:
#             yield MidiEvent(EventKind.CONTROL, tick, channel, None, None, None, None, control)
#
#     def midi_events_from_events2(events: Iterable[Event]) -> Iterable[MidiEvent]:
#         res = peek(iterator=events)
#         if not res:
#             return
#         _, events = res
#         initial = MidiEventsWithTick(
#             tick=tick,
#             midi_events=(event for event in [MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program_, None)])
#         )
#         return functools.reduce(add_midi_event, events, initial)
#
#     def midi_events_from_events(events: Iterator[Event]) -> Iterator[MidiEvent]:
#         res = peek(iterator=events)
#         if not res:
#             return
#         _, events = res
#         nonlocal tick
#         yield MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program_, None)
#         for time, key, duration, velocity, program, control in events:
#             yield MidiEvent(EventKind.NOTE, tick, channel, key, u2t(duration), velocity, program, control)
#             if program:
#                 yield MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program, None)
#             if control:
#                 yield MidiEvent(EventKind.CONTROL, tick, channel, None, None, None, None, control)
#             tick += u2t(time)
#             midi_events_from_events.tick = tick
#
#     return midi_events_from_events2


class Voice(NamedTuple):

    registry: VoiceRegistry = {}
    mappings = {}

    def __call__(self, channel: str, soundfont: str = DEFAULT, bank: int = 0, preset: int = 0):
        def decorator(fn):
            self.registry[fn.__name__] = VoiceArgs(
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


voice = Voice()
