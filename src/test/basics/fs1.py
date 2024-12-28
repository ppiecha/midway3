import time

from src.app.backend import synth

fs = synth.Synth()
fs.start(driver="dsound")
c = 9
b = 128

sfid = fs.sfload("../../../soundfont.sf2")
fs.program_select(c, sfid, b, 0)
print(fs.channel_info(c))

# for b in range(129):
#     for p in range(128):
#         name = fs.sfpreset_name(sfid, b, p)
#         if name:
#             fs.program_select(c, sfid, b, p)
#             print(b, p, name)
#             fs.noteon(c, 60, 120)
#             time.sleep(0.25)
#             fs.noteoff(c, 60)

fs.program_select(c, sfid, 128, 0)
for i in range(60):
    name = fs.program_select(c, sfid, 128, i)
    print(128, i, name)
    fs.noteon(c, 35 + i, 120)
    time.sleep(0.25)
    fs.noteoff(c, i)


# fs.noteon(c, 60, 120)
# fs.noteon(c, 36, 120)
# fs.noteon(c, 37, 120)

# time.sleep(2.0)
#
# fs.noteoff(c, 60)
# fs.noteoff(c, 67)
# fs.noteoff(c, 76)

time.sleep(2.0)

fs.delete()
