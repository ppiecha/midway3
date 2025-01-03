import pytest

from src.app.decorators.voice import voice
from src.app.backend.types import Notes, EventKind, MidiEvent, Program, Tick
from src.app.midi.music_args import MusicArgs
from src.app.decorators.player import player
from src.app.decorators.voice_combination import cmb, events_from_sequences


@voice.channels
def channels_map():
    return {
        "drums": 10,
        "track1": 1,
        "track2": 2,
    }


@voice.soundfonts
def soundfonts_map():
    return {
        "default": "soundfont.sf2",
    }


@pytest.fixture(name="track1")
@voice(channel="track1", soundfont="default", bank=0, preset=0)
def track1():
    return Notes(
        times=(1,),
        keys=(72,),
        durations=(1,),
    )


@pytest.fixture(name="track2")
@voice(channel="track2", soundfont="default", bank=0, preset=12)
def track2():
    return Notes(
        times=(4, 4 / 3),
        keys=(None, 60),
        durations=(4, 4 / 3),
    )


@cmb()
def sequence1():
    return ((track1, track2),)


@cmb()
def sequence2():
    return (
        (track1, track2),
        (track2, track1),
    )


@player(bpm=60, soundfont_path="../..", soundfont="soundfont.sf2", ticks_per_beat=96, start_part=1, end_part=0)
def music():
    return (sequence2,)


@pytest.fixture(name="music_args")
def fixture_music_args():
    return MusicArgs(player=player, track=voice, sequence=cmb, soundfont_ids={"default": 0})


def test_bars(music_args):
    tick, events = events_from_sequences(music_args=music_args, offset=Tick(0))
    assert tick == 96 * 4 * 2
    assert events == [
        MidiEvent(
            kind=EventKind.PROGRAM,
            tick=0,
            channel=1,
            key=None,
            duration=None,
            velocity=None,
            program=Program(sfid=0, bank=0, preset=0),
            control=None,
        ),
        MidiEvent(
            kind=EventKind.NOTE, tick=0, channel=1, key=72, duration=384, velocity=100, program=None, control=None
        ),
        MidiEvent(
            kind=EventKind.PROGRAM,
            tick=0,
            channel=2,
            key=None,
            duration=None,
            velocity=None,
            program=Program(sfid=0, bank=0, preset=12),
            control=None,
        ),
        MidiEvent(
            kind=EventKind.NOTE, tick=0, channel=2, key=None, duration=96, velocity=100, program=None, control=None
        ),
        MidiEvent(
            kind=EventKind.NOTE, tick=96, channel=2, key=60, duration=288, velocity=100, program=None, control=None
        ),
    ]
