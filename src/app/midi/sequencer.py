import os
from contextlib import contextmanager

from src.app.backend.synth import Synth, Sequencer
from src.app.backend.types import Tick, MidiEvent, EventKind, SoundfontIds
from src.app.backend.units import ticks_per_second
from src.app.midi.music import midi_events
from src.app.midi.music_args import MusicArgs
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


@contextmanager
def managed_sequencer(music_args: MusicArgs):
    sequencer = MidiSequencer(music_args=music_args)
    try:
        yield sequencer
    finally:
        sequencer.close()


class MidiSequencer:

    def __init__(self, music_args: MusicArgs):
        self.music_args = music_args
        self.player_args = music_args.player_args()
        self.tpb = self.player_args.ticks_per_beat
        self.soundfonts = music_args.soundfonts()
        self.sequencer = Sequencer(time_scale=ticks_per_second(self.player_args.bpm, self.tpb), use_system_timer=False)
        self.my_seq_id = self.sequencer.register_client("mycallback", self.seq_callback)
        self.synth_seq_id = None
        self.events_iter = None
        self.fs = None

    def play(self):
        self.fs = Synth()
        self.music_args = self.music_args._replace(soundfont_ids=self.get_soundfonts_ids_dict())
        self.synth_seq_id = self.sequencer.register_fluidsynth(self.fs)
        self.fs.start(driver="dsound")
        tick = Tick(self.sequencer.get_tick())
        self.events_iter = midi_events(music_args=self.music_args, tick=tick)
        self.schedule_next_bar(tick)

    def pause(self):
        pass

    def unpause(self):
        pass

    def stop(self):
        self.fs.delete()

    def close(self):
        self.stop()
        self.sequencer.delete()

    def seq_callback(self, time, event, seq, data):
        logger.debug(f"seq_callback: {time}, {event}, {seq}, {data} {Tick(self.tpb).add(time)}")
        self.schedule_next_bar(Tick(self.tpb).add(Tick(time)))

    def schedule_next_callback(self, next_callback_time):
        # I want to be called back before the end of the next sequence
        logger.debug(f"schedule_next_callback: {next_callback_time}")
        self.sequencer.timer(next_callback_time, dest=self.my_seq_id)

    def schedule_next_bar(self, tick: Tick):
        logger.debug(f"schedule_next_bar: {tick}")
        next_start = None
        # Takewhile event is not meta - for instance repeat
        for e in self.events_iter:
            logger.debug(f"{tick} {e}")
            self.sequencer_event(e)
            if e.kind == EventKind.META_END_OF_BAR:
                next_start = e.tick

        logger.debug(f"tt {next_start} {Tick(next_start - self.tpb)}")
        self.schedule_next_callback(Tick(next_start - self.tpb))

    def sequencer_event(self, event: MidiEvent) -> None:
        match event.kind:
            case EventKind.NOTE:
                self.sequencer.note(
                    time=event.tick,
                    channel=event.channel,
                    key=event.key,
                    duration=event.duration,
                    velocity=event.velocity,
                    dest=self.synth_seq_id,
                )
            case EventKind.PROGRAM:
                self.sequencer.program_change(
                    time=event.tick,
                    channel=event.channel,
                    program=event.program,
                    dest=self.synth_seq_id,
                )
            case EventKind.CONTROL:
                self.sequencer.control_change(
                    time=event.tick,
                    channel=event.channel,
                    control=event.control.control,
                    value=event.control.value,
                    dest=self.synth_seq_id,
                )
            case EventKind.META_END_OF_BAR:
                logger.debug(f"[Sequencer add] Skipping meta event {event}")

    def get_soundfonts_ids_dict(self) -> SoundfontIds:
        if not self.fs:
            raise RuntimeError("FluidSynth not defined yet")
        return {
            name: self.fs.sfload(os.path.join(self.player_args.soundfont_path, file_name))
            for name, file_name in self.soundfonts.items()
        }
