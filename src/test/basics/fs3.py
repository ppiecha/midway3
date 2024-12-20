import time

import fluidsynth


def local_file_path(file_name: str) -> str:
    """
    Return a file path to a file that is in the same directory as this file.
    """
    from os.path import dirname, join

    return join(dirname(__file__), file_name)


fs = fluidsynth.Synth()
fs.start(driver="dsound")

sfid = fs.sfload("soundfont.sf2")
fs.program_select(0, sfid, 0, 0)

fs.noteon(0, 60, 30)
time.sleep(0.3)

for i in range(10):
    fs.cc(0, 93, 127)
    fs.pitch_bend(0, i * 512)
    time.sleep(0.1)
fs.noteoff(0, 60)

time.sleep(1.0)

fs.delete()
