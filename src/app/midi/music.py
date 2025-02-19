from typing import Iterator, Callable

from src.app.backend.types import Tick, TrackArgs, MidiEvent, EventKind, Program, Gen, Event, FunctionType
from src.app.decorators.track import events_fn
from src.app.midi.music_args import MusicArgs


def midi_events(music_args: MusicArgs, tick: Tick) -> Gen[MidiEvent]:
    return music_events(music_func=music_args.music_func(), music_args=music_args, tick=tick)


def track_events(track_args: TrackArgs, music_args: MusicArgs, tick: Tick) -> Gen[MidiEvent]:
    # call track function to get notes
    notes = track_args.notes_fn()
    # get events from notes
    events: Gen[Event] = events_fn(notes)
    # prepare midi properties
    channel = music_args.channels()[track_args.channel_name]
    sfid = music_args.soundfont_ids[track_args.soundfont]
    program = Program(sfid, track_args.bank, track_args.preset)
    program_midi_event = MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program, None)
    u2t = music_args.u2t()
    # yield midi events from events
    yield program_midi_event
    for time, key, duration, velocity, program, control in events:
        yield MidiEvent(EventKind.NOTE, tick, channel, key, u2t(duration), velocity, program, control)
        if program:
            yield MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program, None)
        if control:
            yield MidiEvent(EventKind.CONTROL, tick, channel, None, None, None, None, control)
        tick = tick.add(time)
    yield MidiEvent(EventKind.META_END_OF_USER_SEQ, tick, channel, None, None, None, None, None)


# def merge_events(iterator: Iterator[Iterator[MidiEvent]]) -> Iterator[MidiEvent]:
#     return itertools.chain(*iterator)
#
#
# def mix_events(note_fns: Iterable[NotesFunc], music_args: MusicArgs, tick: Tick) -> Iterator[Iterator[MidiEvent]]:
#     # transforms mix track functions to their corresponding track args
#     track_args_iterator = map(lambda fn: music_args.track_args_by_name(fn.__name__), note_fns)
#     # creates one arg function which gets events based on track args
#     track_events_from_track_args = partial(track_events, music_args=music_args, tick=tick)
#     # transforms track args to iterator of iterator of events
#     return map(track_events_from_track_args, track_args_iterator)


def function_type(func_name, music_args: MusicArgs) -> FunctionType:
    if func_name in music_args.track_registry():
        return FunctionType.TRACK
    if func_name in music_args.mix_registry():
        return FunctionType.MIX
    if func_name in music_args.chain_registry():
        return FunctionType.CHAIN
    raise ValueError(
        f"Cannot find function {func_name} in registries\n"
        f"{music_args.track_registry()}\n{music_args.mix_registry()}\n{music_args.chain_registry()}"
    )


def music_events(music_func: Callable, music_args: MusicArgs, tick: Tick) -> Gen[MidiEvent]:
    match function_type(func_name=music_func.__name__, music_args=music_args):
        case FunctionType.TRACK:
            track_args = music_args.track_args_by_name(music_func.__name__)
            yield from track_events(track_args=track_args, music_args=music_args, tick=tick)
        case FunctionType.MIX:
            for func in music_func():
                yield from music_events(music_func=func, music_args=music_args, tick=tick)
        case FunctionType.CHAIN:
            next_tick = tick
            for func in music_func():
                for event in music_events(music_func=func, music_args=music_args, tick=next_tick):
                    if event.kind == EventKind.META_END_OF_USER_SEQ:
                        next_tick = event.tick
                    yield event
