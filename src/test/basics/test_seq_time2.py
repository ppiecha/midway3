import time

from fluidsynth import Sequencer, Synth

from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)

# FIRST ITERATION
# seq representation

def gen_notes(synthSeqID):
    for i in range(8):
        yield (i + 1) * 250, 0, 60 + (2 * i), 250, 127, synthSeqID

def run_sequencer() -> None:

    def seq_callback(time, event, seq, data):
        logger.debug(f"seq_callback: {time}, {event}, {seq}, {data}")
        schedule_next_bar(time)

    def schedule_next_callback(next_callback_time):
        # I want to be called back before the end of the next sequence
        logger.debug(f"schedule_next_callback: {next_callback_time}")
        sequencer.timer(next_callback_time, dest=mySeqID)

    def schedule_next_bar(now):
        logger.debug(f"schedule_next_bar: {now}")
        for time, channel, key, duration, velocity, dest in gen_notes(synthSeqID):
        # sequencer.note(int(now + offset), 0, 60, duration=125, velocity=127, dest=synthSeqID)
            sequencer.note(int(now + time), channel, key, duration=duration, velocity=velocity, dest=dest)
        schedule_next_callback(now + 2000)


    fs = Synth()
    fs.start(driver='dsound')
    sfid = fs.sfload("../../../soundfont.sf2")
    fs.program_select(0, sfid, 0, 0)
    # fs.noteon(0, 60, 100)
    sequencer = Sequencer(use_system_timer=False)
    synthSeqID = sequencer.register_fluidsynth(fs)
    mySeqID = sequencer.register_client("mycallback", seq_callback)
    now = sequencer.get_tick()
    schedule_next_bar(now, 250)
    time.sleep(10)
    logger.debug('starting to delete')
    sequencer.delete()
    fs.delete()

run_sequencer()
