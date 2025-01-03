import os.path
import time
from functools import wraps

from typing_extensions import NamedTuple

from src.app.backend.synth import Synth, Sequencer
from src.app.backend.types import PlayerArgs, MidiEvent, Tick, EventKind, Soundfonts, SoundfontIds
from src.app.midi.music_args import MusicArgs
from src.app.backend.units import ticks_per_second
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


class Player(NamedTuple):

    args: list[PlayerArgs] = []

    def __call__(
        self,
        bpm: int,
        soundfont_path: str,
        soundfont: str,
        ticks_per_beat: int = 96,
        start_part: int = 1,
        end_part: int | None = None,
    ):
        def decorator(fn):
            self.args.append(PlayerArgs(bpm, soundfont_path, soundfont, ticks_per_beat, fn))

            @wraps(fn)
            def inner(*args_, **kwargs):
                return fn(*args_, **kwargs)

            return inner

        return decorator


player = Player()
