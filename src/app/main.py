import os.path

from src.app.backend.types import MusicArgs, Notes
from src.app.utils.file_generator import file_content, new_file
from src.app.utils.file_ops import read_file
from src.app.utils.logger import get_console_logger
from src.app.backend.tracks import track
from src.app.midi.sequences import sequence
from src.app.midi.player import player, events_to_play, sequencer_wrapper

logger = get_console_logger(__name__)

if __name__ == "__main__":
    file_name = "template1.py"
    path = "../../projects/test1/"
    new_file(file_name=file_name, path=path, file_content_fn=file_content)
    spec = read_file(os.path.join(path, file_name))
    # logger.debug(spec)
    exec(spec)
    sequencer = sequencer_wrapper(MusicArgs(player=player, track=track, sequence=sequence))
