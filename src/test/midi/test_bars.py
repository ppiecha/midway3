import pytest

from src.app.backend.tracks import track
from src.app.backend.types import MusicArgs, Notes, EventKind, MidiEvent, Program
from src.app.midi.player import player, events_to_play
from src.app.midi.sequences import sequence


@track.channels
def channels_map():
    return {
        "drums": 10,
        "track1": 1,
        "track2": 2,
    }


@track.soundfonts
def soundfonts_map():
    return {
        "default": "soundfont.sf2",
    }


@pytest.fixture(name="track1")
@track(channel="track1", soundfont="default", bank=0, preset=0)
def track1():
    return Notes(
        times=(1,),
        keys=(72,),
        durations=(1,),
    )


@pytest.fixture(name="track2")
@track(channel="track2", soundfont="default", bank=0, preset=12)
def track2():
    return Notes(
        times=(4, 4 / 3),
        keys=(None, 60),
        durations=(4, 4 / 3),
    )


@sequence()
def sequence1():
    return ((track1, track2),)


@sequence()
def sequence2():
    return (
        (track1, track2),
        (track2, track1),
    )


@player(bpm=60, soundfont_path="../..", soundfont="soundfont.sf2", ticks_per_beat=96, start_part=1, end_part=0)
def music():
    return (sequence1,)


@pytest.fixture(name="music_args")
def fixture_music_args():
    return MusicArgs(player=player, track=track, sequence=sequence, soundfont_ids={"default": 0})


def test_bars(music_args):
    tick, events = events_to_play(music_args=music_args, offset=0)
    assert tick == 96 * 4  # * 3 # 3 bars
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