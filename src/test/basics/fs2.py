import time

from src.app.backend import synth as fluidsynth

seqduration = 1000


def schedule_next_callback():
    # I want to be called back before the end of the next sequence
    callbackdate = int(now + seqduration / 2)
    sequencer.timer(callbackdate, dest=mySeqID)


def schedule_next_sequence():
    global now
    print("schedule_next_sequence", now)
    # the sequence to play
    # the beat : 2 beats per sequence
    sequencer.note(int(now + seqduration * 1 / 2), 0, 60, duration=250, velocity=80, dest=synthSeqID)
    sequencer.note(int(now + seqduration * 2 / 2), 0, 60, duration=250, velocity=80, dest=synthSeqID)
    # melody
    sequencer.note(int(now + seqduration * 1 / 10), 1, 45, duration=250, velocity=int(127 * 2 / 3), dest=synthSeqID)
    sequencer.note(int(now + seqduration * 4 / 10), 1, 50, duration=250, velocity=int(127 * 2 / 3), dest=synthSeqID)
    sequencer.note(int(now + seqduration * 8 / 10), 1, 55, duration=250, velocity=int(127 * 3 / 3), dest=synthSeqID)
    # so that we are called back early enough to schedule the next sequence
    schedule_next_callback()

    now = now + seqduration


def seq_callback(time, event, seq, data):
    print("call schedule_next_sequence in seq_callback")
    schedule_next_sequence()


def local_file_path(file_name: str) -> str:
    """
    Return a file path to a file that is in the same directory as this file.
    """
    from os.path import dirname, join

    return join(dirname(__file__), file_name)


if __name__ == "__main__":
    global sequencer, fs, mySeqID, synthSeqID, now
    fs = fluidsynth.Synth()
    fs.start(driver="dsound")
    sfid = fs.sfload("../../../soundfont.sf2")
    fs.program_select(0, sfid, 0, 0)
    fs.program_select(1, sfid, 0, 0)  # use the same program for channel 2 for cheapness

    sequencer = fluidsynth.Sequencer(use_system_timer=False)
    synthSeqID = sequencer.register_fluidsynth(fs)
    mySeqID = sequencer.register_client("mycallback", seq_callback)
    now = sequencer.get_tick()
    print("before schedule_next_sequence")
    schedule_next_sequence()
    time.sleep(1)
    print(1)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print(1)
    time.sleep(1)
    print("done")
    sequencer.delete()
    fs.delete()
