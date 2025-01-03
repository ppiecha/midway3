import functools
import itertools
from collections.abc import Iterable, Iterator
from functools import wraps
from typing import NamedTuple

from src.app.decorators.voice import events_fn
from src.app.backend.types import (
    MidiEvent,
    PlayerArgs,
    VoiceRegistry,
    Tick,
    Channels,
    Program,
    MidiEventsWithTick,
    VoiceCombinationRegistry,
)
from src.app.midi.music_args import MusicArgs

from src.app.utils.iter import empty_gen
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


class VoiceCombination(NamedTuple):

    registry: VoiceCombinationRegistry = {}

    def __call__(self):

        def decorator(fn):

            self.registry[fn.__name__] = fn

            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)

            return inner

        return decorator


cmb = VoiceCombination()


# def events_from_sequences(music_args: MusicArgs, offset: Tick = Tick(0)) -> MidiEventsWithTick:
#
#     track = music_args.voice
#     tracks: VoiceRegistry = track.registry
#     channels: Channels = track.channels_map_func()
#     u2t = music_args.player.args[0].tick_from_unit
#
#     setattr(Tick, "tick_from_unit", music_args.player.args[0].tick_from_unit)
#
#     def add_sequence(events_with_tick: MidiEventsWithTick, seq_func: SequenceFunc) -> MidiEventsWithTick:
#         seq = VoiceCombination(seq_func())
#         return MidiEventsWithTick(
#             tick=events_with_tick.tick.add(len(seq)),
#             midi_events=itertools.chain(
#                 events_with_tick.midi_events, events_from_bars(seq.bars, events_with_tick.tick)
#             ),
#         )
#
#     def events_from_bar(bar: Bar, tick: Tick) -> Iterable[MidiEvent]:
#         def from_notes_fn(notes_fn):
#             notes = notes_fn()
#             events = events_fn(notes)
#             track_args = tracks[notes_fn.__name__]
#             sfid = music_args.soundfont_ids[track_args.soundfont]
#             program = Program(sfid, track_args.bank, track_args.preset)
#             channel = channels[track_args.channel_name]
#             midi_events_fn = args_wrapper(tick, channel, program, u2t)
#             return midi_events_fn(events)
#
#
#
#     def add_bar(events_with_tick: MidiEventsWithTick, bar: Bar) -> MidiEventsWithTick:
#
#         # bar = Iterable[NotesFunc]
#         return MidiEventsWithTick(
#             tick=events_with_tick.tick.add(len(bar)),
#             midi_events=itertools.chain(
#                 events_with_tick.midi_events, events_from_bar(bar, events_with_tick.tick)
#             )
#         )
#
#     def events_from_bars(bars: Iterable[Bar], tick: Tick) -> Iterable[MidiEvent]:
#         initial = MidiEventsWithTick(tick=offset, midi_events=empty_gen())
#         return functools.reduce(add_bar, bars, initial)
#
#     sequences: Sequences = music_args.player.args[0].music()
#     initial = MidiEventsWithTick(tick=offset, midi_events=empty_gen())
#     return functools.reduce(add_sequence, sequences, initial)
#
#
# def events_from_sequences3(music_args: MusicArgs, offset: Tick = 0) -> Iterator[MidiEvent]:
#     track = music_args.voice
#     tracks: VoiceRegistry = track.registry
#     channels: Channels = track.channels_map_func()
#     player_args: PlayerArgs = music_args.player.args
#     sequences = music_args.player.args.sequences()
#     u2t = player_args.tick_from_unit
#     for sequence in sequences:
#         for bar in sequence():
#             for track_fn in bar:
#                 tick = offset
#                 logger.debug(f"{tick = }")
#                 track_args = tracks[track_fn.__name__]
#                 sfid = music_args.soundfont_ids[track_args.soundfont]
#                 program = Program(sfid, track_args.bank, track_args.preset)
#                 channel = channels[track_args.channel_name]
#                 midi_events_fn = args_wrapper(tick, channel, program, u2t)
#                 yield from midi_events_fn(events_fn(track_args.notes()))
#                 tick = midi_events_fn.tick
#             sequence_length = tick
#             logger.debug(f"{sequence_length = }")
#             offset += sequence_length
#             pass
#     return offset
