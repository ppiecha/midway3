import pytest

from src.app.decorators.voice import events_fn
from src.app.backend.types import Event


def test_non_note():
    with pytest.raises(StopIteration):
        event = next(iter(events_fn(None)))


def test_empty_note(empty_note):
    with pytest.raises(StopIteration):
        event = next(iter(events_fn(empty_note)))


def test_one_note(one_note_event):
    assert one_note_event == Event(time=4, key=60, duration=4, velocity=100, program=None, control=None)


def test_two_notes(two_notes):
    it = iter(events_fn(two_notes))
    event1 = next(it)
    assert event1 == Event(time=4, key=None, duration=None, velocity=100, program=None, control=None)
    event2 = next(it)
    assert event2 == Event(time=4, key=60, duration=8, velocity=100, program=None, control=None)
    with pytest.raises(StopIteration):
        event = next(it)
