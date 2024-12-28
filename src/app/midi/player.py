import os.path
import time
from collections.abc import Iterable
from functools import wraps

from src.app.backend.synth import Synth, Sequencer
from src.app.backend.types import PlayerArgs, MusicArgs, MidiEvent, Tick, EventKind, Tracks, Soundfonts, SoundfontIds
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
    all_events = []
    while 1:
        try:
            all_events.append(next(events))
        except StopIteration as e:
            return e.value, all_events


def sequencer_wrapper(music_args: MusicArgs):

    player_args = music_args.player.args
    u2t = player_args.u2t
    track = music_args.track
    soundfonts: Soundfonts = track.soundfonts_map_func()

    def seq_callback(time, event, seq, data):
        logger.debug(f"seq_callback: {time}, {event}, {seq}, {data}")
        schedule_next_bar(time + u2t(2))

    def schedule_next_callback(next_callback_time):
        # I want to be called back before the end of the next sequence
        logger.debug(f"schedule_next_callback: {next_callback_time}")
        sequencer.timer(next_callback_time, dest=my_seq_id)

    def schedule_next_bar(offset):
        logger.debug(f"schedule_next_bar: {offset}")
        tick, events = events_to_play(music_args=music_args, offset=offset)
        for e in events:
            logger.debug(e)
            sequencer_event(e)

        schedule_next_callback(offset + int(tick / 2))

    def sequencer_event(event: MidiEvent) -> None:
        match event.kind:
            case EventKind.NOTE:
                sequencer.note(
                    time=event.tick,
                    channel=event.channel,
                    key=event.key,
                    duration=event.duration,
                    velocity=event.velocity,
                    dest=synth_seq_id,
                )
            case EventKind.PROGRAM:
                sequencer.program_change(
                    time=event.tick,
                    channel=event.channel,
                    program=event.program,
                    dest=synth_seq_id,
                )
            case EventKind.CONTROL:
                sequencer.control_change(
                    time=event.tick,
                    channel=event.channel,
                    control=event.control.control,
                    value=event.control.value,
                    dest=synth_seq_id,
                )

    def load_soundfonts() -> SoundfontIds:
        return {
            name: fs.sfload(os.path.join(player_args.soundfont_path, file_name))
            for name, file_name in soundfonts.items()
        }

    fs = Synth()
    fs.start(driver="dsound")
    music_args = music_args._replace(soundfont_ids=load_soundfonts())
    sequencer = Sequencer(
        time_scale=ticks_per_second(player_args.bpm, player_args.ticks_per_beat), use_system_timer=False
    )
    synth_seq_id = sequencer.register_fluidsynth(fs)
    my_seq_id = sequencer.register_client("mycallback", seq_callback)
    schedule_next_bar(sequencer.get_tick())
    time.sleep(20)
    logger.debug("starting to delete")
    sequencer.delete()
    fs.delete()
