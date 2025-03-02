from functools import wraps

from typing_extensions import NamedTuple

from src.app.backend.types import PlayerArgs
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
        numerator=4,
        denominator=4,
        repeat=1,
    ):
        def decorator(fn):
            self.args.append(
                PlayerArgs(
                    bpm=bpm,
                    soundfont_path=soundfont_path,
                    soundfont=soundfont,
                    ticks_per_beat=ticks_per_beat,
                    numerator=numerator,
                    denominator=denominator,
                    repeat=repeat,
                    music_func=fn,
                )
            )

            @wraps(fn)
            def inner(*args_, **kwargs):
                return fn(*args_, **kwargs)

            return inner

        return decorator


player = Player()
