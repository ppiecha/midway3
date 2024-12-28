from collections.abc import Iterable
from functools import partial

import pytest

from src.app.backend.tracks import events_fn
from src.app.backend.types import Notes, Event
from src.app.backend.units import unit2tick


@pytest.fixture(name="empty_note")
def fixture_empty_note() -> Notes:
    return Notes(
        times=(),
    )


@pytest.fixture(name="one_note")
def fixture_one_note() -> Notes:
    return Notes(
        times=(4,),
        keys=(60,),
        durations=(4,),
    )


@pytest.fixture(name="two_notes")
def fixture_two_note() -> Notes:
    return Notes(
        times=(
            4,
            4,
        ),
        keys=(
            None,
            60,
        ),
        durations=(None, 8),
    )


@pytest.fixture(name="one_note_event")
def fixture_one_note_event(one_note) -> Iterable[Event]:
    return next(events_fn(one_note))


@pytest.fixture(name="u2t60")
def fixture_u2t60():
    return partial(unit2tick, bpm=60, ticks_per_beat=96)
