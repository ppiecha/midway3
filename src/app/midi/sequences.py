from collections.abc import Iterable, Callable
from functools import wraps, partial

from src.app.backend.tracks import events_fn, args_wrapper
from src.app.backend.types import (
    Sequence,
    MidiEvent,
    UnitToTick,
    MusicArgs,
    PlayerArgs,
    Tracks,
    Tick,
    Channels,
    Program,
)
from src.app.backend.units import unit2tick
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def sequence_wrapper():
    sequences = {}

    def outer():
        def decorator(fn):
            sequences[fn.__name__] = fn

            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)

            return inner

        return decorator

    outer.sequences = sequences
    return outer


sequence = sequence_wrapper()


def events_from_sequences(music_args: MusicArgs, offset: Tick = 0) -> Iterable[MidiEvent]:
    track = music_args.track
    tracks: Tracks = track.tracks
    channels: Channels = track.channels_map_func()
    player_args: PlayerArgs = music_args.player.args
    sequences = music_args.player.args.sequences()
    u2t = player_args.u2t
    for sequence in sequences:
        for bar in sequence():
            for track_fn in bar:
                tick = offset
                logger.debug(f"{tick = }")
                track_args = tracks[track_fn.__name__]
                sfid = music_args.soundfont_ids[track_args.soundfont]
                program = Program(sfid, track_args.bank, track_args.preset)
                channel = channels[track_args.channel_name]
                midi_events_fn = args_wrapper(tick, channel, program, u2t)
                yield from midi_events_fn(events_fn(track_args.notes()))
                tick = midi_events_fn.tick
            sequence_length = tick
            logger.debug(f"{sequence_length = }")
        offset += sequence_length
    return offset
