import os.path
import time

# do not remove
from src.app.backend.types import Tick, Notes
from src.app.midi.music_args import MusicArgs
from src.app.midi.sequencer import managed_sequencer
from src.app.utils.file_generator import file_content, new_file
from src.app.utils.file_ops import read_file
from src.app.utils.logger import get_console_logger
from src.app.decorators.track import track
from src.app.decorators.track_mix import mix
from src.app.decorators.track_chain import chain
from src.app.decorators.player import player

logger = get_console_logger(__name__)

if __name__ == "__main__":
    file_name = "template1.py"
    path = "../../projects/test1/"
    new_file(file_name=file_name, path=path, file_content_fn=file_content)
    spec = read_file(os.path.join(path, file_name))
    exec(spec)
    music_args = MusicArgs(player=player, track=track, mix=mix, chain=chain, soundfont_ids=None)
    # music_args = music_args._replace(soundfont_ids={"default": 1})
    # for e in midi_events(music_args, tick=Tick(0)):
    #     print(e)
    with managed_sequencer(music_args=music_args) as sequencer:
        sequencer.play()
        time.sleep(10)
