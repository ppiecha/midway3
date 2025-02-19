from functools import wraps
from typing import NamedTuple

from src.app.backend.types import (
    TrackMixRegistry,
)

from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


class TrackMix(NamedTuple):

    registry: TrackMixRegistry = {}

    def __call__(self):

        def decorator(fn):

            self.registry[fn.__name__] = fn

            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)

            return inner

        return decorator


mix = TrackMix()
