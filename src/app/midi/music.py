import itertools
from collections.abc import Iterable
from functools import partial

from src.app.backend.types import Tick, MidiEvents, VoiceArgs, MidiEvent, EventKind, Program, NotesFunc
from src.app.decorators.voice import events_fn
from src.app.midi.music_args import MusicArgs


def midi_events(music_args: MusicArgs, tick: Tick) -> MidiEvents:
    return mix_events(mix=music_args.music(), music_args=music_args, tick=tick)


def voice_args_events(voice_args: VoiceArgs, music_args: MusicArgs, tick: Tick) -> MidiEvents:
    notes = voice_args.notes_fn()
    events = events_fn(notes)
    channel = music_args.channels()[voice_args.channel_name]
    sfid = music_args.soundfont_ids[voice_args.soundfont]
    program = Program(sfid, voice_args.bank, voice_args.preset)
    program_event = MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program, None)
    u2t = music_args.u2t()
    yield program_event
    for time, key, duration, velocity, program, control in events:
        yield MidiEvent(EventKind.NOTE, tick, channel, key, u2t(duration), velocity, program, control)
        if program:
            yield MidiEvent(EventKind.PROGRAM, tick, channel, None, None, None, program, None)
        if control:
            yield MidiEvent(EventKind.CONTROL, tick, channel, None, None, None, None, control)
        tick = tick.add(time)
    yield MidiEvent(EventKind.META_END_OF_USER_SEQ, tick, channel, None, None, None, None, None)


def add_midi_events(iterable: Iterable[MidiEvents]) -> MidiEvents:
    return itertools.chain(*iterable)


def mix_events(mix: Iterable[NotesFunc], music_args: MusicArgs, tick: Tick) -> MidiEvents:
    voice_args_iter = map(lambda fn: music_args.voice_args_by_name(fn.__name__), mix)
    fn = partial(voice_args_events, music_args=music_args, tick=tick)
    events_iter = map(fn, voice_args_iter)
    return add_midi_events(events_iter)
