import time

from fluidsynth import Sequencer, Synth


def run_sequencer() -> None:

    def seq_callback(time, event, seq, data):
        print("seq_callback", time, event, seq, data)
        schedule_next_sequence(time, 250)

    def schedule_next_callback(next_callback_time):
        # I want to be called back before the end of the next sequence
        print("schedule_next_callback", next_callback_time)
        sequencer.timer(next_callback_time, dest=mySeqID)

    def schedule_next_sequence(now, offset):
        print("schedule_next_sequence", now)
        sequencer.note(int(now + offset), 0, 60, duration=125, velocity=127, dest=synthSeqID)
        schedule_next_callback(now + 250)

    fs = Synth()
    fs.start(driver="dsound")
    sfid = fs.sfload("../../../soundfont.sf2")
    fs.program_select(0, sfid, 0, 0)
    # fs.noteon(0, 60, 100)
    sequencer = Sequencer(use_system_timer=False)
    synthSeqID = sequencer.register_fluidsynth(fs)
    mySeqID = sequencer.register_client("mycallback", seq_callback)
    now = sequencer.get_tick()
    schedule_next_sequence(now, 250)
    time.sleep(5)
    print("starting to delete")
    sequencer.delete()
    fs.delete()


run_sequencer()
