import os.path
import time
from collections.abc import Iterable
from functools import wraps
from typing import Callable, Dict

from fluidsynth import Synth, Sequencer

from src.app.backend.types import TrackArgs, PlayerArgs, MusicArgs, MidiEvent, Tick, EventKind
from src.app.backend.units import ticks_per_second
from src.app.midi.sequences import events_from_sequences
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def player_wrapper():
    def outer(
        bpm: int,
        soundfont_path: str,
        soundfont: str,
        ticks_per_beat: int = 96,
        start_part: int = 1,
        end_part: int | None = None,
    ):
        def decorator(fn):
            outer.args = PlayerArgs(bpm, soundfont_path, soundfont, ticks_per_beat, fn)

            @wraps(fn)
            def inner(*args_, **kwargs):
                return fn(*args_, **kwargs)

            return inner

        return decorator

    return outer


player = player_wrapper()


def events_to_play(music_args: MusicArgs, offset: Tick = 0) -> tuple[Tick, Iterable[MidiEvent]]:
    events = events_from_sequences(music_args=music_args, offset=offset)
    all_events = set()
    while 1:
        try:
            all_events.add(next(events))
        except Exception as e:
            return e.value, all_events

def sequencer_wrapper(music_args: MusicArgs):

    player_args = music_args.player.args
    u2t = player_args.u2t

    def seq_callback(time, event, seq, data):
        logger.debug(f"seq_callback: {time}, {event}, {seq}, {data}")
        schedule_next_bar(time + u2t(2))

    def schedule_next_callback(next_callback_time):
        # I want to be called back before the end of the next sequence
        logger.debug(f"schedule_next_callback: {next_callback_time}")
        sequencer.timer(next_callback_time, dest=mySeqID)

    def schedule_next_bar(offset):
        logger.debug(f"schedule_next_bar: {offset}")
        tick, events = events_to_play(music_args=music_args, offset=offset)
        for e in sorted(events, key=lambda x: x.tick):
            if e.kind == EventKind.NOTE:
                logger.debug(e)
                sequencer.note(
                    time=e.tick,
                    channel=e.channel,
                    key=e.key,
                    duration=e.duration,
                    velocity=e.velocity,
                    dest=synthSeqID)
        schedule_next_callback(offset + int(tick/2))

    player_args: PlayerArgs = music_args.player.args
    fs = Synth()
    fs.start(driver="dsound")
    sfid = fs.sfload(os.path.join(player_args.soundfont_path, player_args.soundfont))
    fs.program_select(0, sfid, 0, 0)
    fs.program_select(1, sfid, 0, 0)
    fs.program_select(10, sfid, 0, 0)
    sequencer = Sequencer(time_scale=ticks_per_second(player_args.bpm, player_args.ticks_per_beat), use_system_timer=False)
    synthSeqID = sequencer.register_fluidsynth(fs)
    mySeqID = sequencer.register_client("mycallback", seq_callback)
    schedule_next_bar(sequencer.get_tick())
    time.sleep(10)
    logger.debug("starting to delete")
    sequencer.delete()
    fs.delete()

