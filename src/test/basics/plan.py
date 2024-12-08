# Program is a python file which defines function with annotations
# Generally to annotate all params like bpm, soundfont, etc.
# Annotation to define voice/track/version
import time
from collections import defaultdict
from functools import partial, wraps
from typing import NamedTuple, Optional, Iterator, Iterable

from fluidsynth import Synth, Sequencer

from src.app.backend import units
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


# reqs
# @midi
# @midi(kind = 'bpm', 'bpm', value = 120)
# @midi(kind = 'soundfont', name = 'main')
# @midi(kind = 'track', name = 'track1', channel = 0, font = 'defined1', bank = 0, preset = 0)
# controls

class TrackOpt(NamedTuple):
    name: str
    channel: int = 0
    font: str = 'default'
    bank: int = 0
    preset: int = 0
    active: bool = True

def track():
    midi_dict = defaultdict(list)
    def midi_track(channel: str = 'piano', font: str = "default", bank: int = 0, preset: int = 0, active: bool = True):
        def decorator(fn):
            midi_dict[(channel, font, bank, preset, active)].append(fn)
            @wraps(fn)
            def inner(*args, **kwargs):
                return fn(*args, **kwargs)
            return inner
        return decorator
    midi_track.midi_dict = midi_dict
    return midi_track

channels = {
    'drums': 9,
    'bass' : 0,
    'piano': 1
}

track = track()


class Notes(NamedTuple):
    times: Iterable[float]
    keys: Iterable[int|None]
    durations: Iterable[float]
    velocities: Iterable[int]|None = None


@track(channel='piano', font="metronome")
def metronome():
    return Notes(
        times      = (4, ) * 4,
        keys       = (90,) * 4,
        durations  = (64, ) * 4,
        velocities = (100,) * 4
    )

@track(font="main2", active=True)
def track1():
    seq = (4, 8, 8, 4, 4)
    return Notes(
        times      = (4, 8, 8, 4, 4),
        keys       = (60, None, 63, 63, 60),
        durations  = (4, 8, 8, 4, 4),
        velocities = (100,) * 5
    )

sequence = {
    'drums': (metronome, metronome)
}

print(type(metronome), metronome.__name__, metronome())

def run_sequencer() -> None:

    BPM = 60
    TPB = 96
    trans = partial(units.unit2tick, bpm = BPM, ticks_per_beat= TPB )
    print('trans', trans, trans(4))

    def seq_callback(time, event, seq, data):
        logger.debug(f"seq_callback: {time}, {event}, {seq}, {data}")
        schedule_next_bar(time + trans(2))

    def schedule_next_callback(next_callback_time):
        # I want to be called back before the end of the next sequence
        logger.debug(f"schedule_next_callback: {next_callback_time}")
        sequencer.timer(next_callback_time, dest=mySeqID)

    def schedule_next_bar(now):
        logger.debug(f"schedule_next_bar: {now}")
        for (channel, font, bank, preset, active), fns in track.midi_dict.items():
            if not active:
                continue
            for fn in fns:
                notes = []
                cmp = fn()
                t = now
                print(list(zip(cmp.times, cmp.keys, cmp.durations, cmp.velocities)))
                for time, key, duration, velocity in zip(cmp.times, cmp.keys, cmp.durations, cmp.velocities):
                    if key is not None:
                        notes.append((t, key, trans(duration)))
                        sequencer.note(int(t), 0, key, duration=trans(duration), velocity=velocity, dest=synthSeqID)
                        t += trans(time)
                logger.debug(notes)
        schedule_next_callback(now + trans(2))
    logger.debug(track.midi_dict)
    fs = Synth()
    fs.start(driver='dsound')
    sfid = fs.sfload("../../../soundfont.sf2")
    fs.program_select(0, sfid, 0, 0)
    # fs.noteon(0, 60, 100)
    sequencer = Sequencer(time_scale=units.ticks_per_second(BPM, TPB), use_system_timer=False)
    synthSeqID = sequencer.register_fluidsynth(fs)
    mySeqID = sequencer.register_client("mycallback", seq_callback)
    schedule_next_bar(sequencer.get_tick())
    time.sleep(10)
    logger.debug('starting to delete')
    sequencer.delete()
    fs.delete()

run_sequencer()