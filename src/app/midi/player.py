import inspect
from functools import wraps
from typing import NamedTuple, Callable, Dict

from src.app.backend.tracks import TrackArgs
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


class PlayerArgs(NamedTuple):
    bpm: int
    soundfont_path: str
    ticks_per_beat: int
    sequence: Callable


def player_wrapper():
    def outer(bpm: int, soundfont_path: str, ticks_per_beat: int = 96, start_part: int = 1, end_part: int = 0):
        def decorator(fn):
            outer.args = PlayerArgs(bpm, soundfont_path, ticks_per_beat, fn)

            @wraps(fn)
            def inner(*args_, **kwargs):
                return fn(*args_, **kwargs)

            return inner

        return decorator

    return outer


player = player_wrapper()


def play(player, track, sequence):
    # logger.debug(track.tracks)
    player_args: PlayerArgs = player.args
    # logger.debug(inspect.getclosurevars(track.channels).nonlocals)
    channels: Dict[str, int] = track.channels_map_func()
    # logger.debug(channels)
    tracks: Dict[str, TrackArgs] = track.tracks
    sequences: Dict[str, Callable] = sequence.sequences
    sequence = player_args.sequence()
    logger.debug(sequence)
