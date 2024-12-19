from functools import wraps
from typing import Callable, Dict

from src.app.backend.types import TrackArgs, PlayerArgs, MusicArgs
from src.app.midi.sequences import events_from_sequences
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def player_wrapper():
    def outer(
        bpm: int,
        soundfont_path: str,
        soundfont: str,
        ticks_per_beat: int = 96,
        start_part: int = 1,
        end_part: int | None = None,
    ):
        def decorator(fn):
            outer.args = PlayerArgs(bpm, soundfont_path, soundfont, ticks_per_beat, fn)

            @wraps(fn)
            def inner(*args_, **kwargs):
                return fn(*args_, **kwargs)

            return inner

        return decorator

    return outer


player = player_wrapper()


def play(music_args: MusicArgs):
    # logger.debug(track.tracks)
    player_args: PlayerArgs = music_args.player.args
    # logger.debug(inspect.getclosurevars(track.channels).nonlocals)
    channels: Dict[str, int] = music_args.track.channels_map_func()
    # logger.debug(channels)
    tracks: Dict[str, TrackArgs] = music_args.track.tracks
    # sequences: Dict[str, Callable] = music_args.sequence.sequences
    sequences = player_args.sequences()
    events = events_from_sequences(sequences=sequences, music_args=music_args, offset=0)
    for event in list(events):
        logger.debug(event)
