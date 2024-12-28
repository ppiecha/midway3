from src.app.backend.tracks import args_wrapper, events_fn
from src.app.backend.types import Program, EventKind, MidiEvent


def test_none_note(u2t60):
    midi_events_fn = args_wrapper(tick=0, channel=0, program_=Program(0, 0, 0), u2t=u2t60)
    midi_events = list(midi_events_fn(events_fn(None)))
    assert not midi_events


def test_empty_note_midi_event(empty_note, u2t60):
    midi_events_fn = args_wrapper(tick=0, channel=0, program_=Program(0, 0, 0), u2t=u2t60)
    midi_events = list(midi_events_fn(events_fn(empty_note)))
    assert not midi_events


def test_one_note_midi_event(one_note_event, u2t60):
    midi_events_fn = args_wrapper(tick=0, channel=0, program_=Program(0, 0, 0), u2t=u2t60)
    midi_events = list(midi_events_fn(iter([one_note_event])))
    assert midi_events == [
        MidiEvent(
            kind=EventKind.PROGRAM,
            tick=0,
            channel=0,
            key=None,
            duration=None,
            velocity=None,
            program=Program(sfid=0, bank=0, preset=0),
            control=None,
        ),
        MidiEvent(
            kind=EventKind.NOTE, tick=0, channel=0, key=60, duration=96, velocity=100, program=None, control=None
        ),
    ]
