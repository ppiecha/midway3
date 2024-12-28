import time
from src.app.backend import synth as fluidsynth

fs = fluidsynth.Synth()
fs.start(driver="dsound")
c = 0

sfid = fs.sfload("../../../soundfont.sf2")
lst = [(b, p, fs.sfpreset_name(sfid, b, p)) for b in range(130) for p in range(130)]
for b, p, name in [item for item in lst if item[2]]:
    print(b, p, name)
# fs.program_select(c, sfid, 0, 0)
#
# fs.noteon(c, 60, 90)
# fs.noteon(c, 67, 90)
# fs.noteon(c, 76, 90)
#
# time.sleep(2.0)
#
# fs.noteoff(c, 60)
# fs.noteoff(c, 67)
# fs.noteoff(c, 76)
#
# time.sleep(2.0)
#
# fs.delete()
