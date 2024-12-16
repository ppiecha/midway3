import os
from typing import Callable

from src.app.utils.file_ops import write_file
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def new_file(file_name: str, path: str = '', file_content_fn: Callable = None):
    full_path = os.path.join(path, file_name)
    logger.debug(f'{full_path = }')
    write_file(full_path=full_path, content=file_content_fn(file_name))

def file_content(file_name: str) -> str:
    file_name = f'# {file_name}'

    channels = ('@track.channels',
                'def channels_map():',
                '\treturn {',
                '\t\t"drums":    9,',
                '\t\t"bass":     0,',
                '}')
    channels = '\n'.join(channels)

    soundfonts = ('@track.soundfonts',
                  'def soundfonts_map():',
                  '\treturn {',
                  '\t\t"default": "soundfont.sf2",',
                  '}')
    soundfonts = '\n'.join(soundfonts)

    drums = ('@track(channel="drums", font="default", bank=0, preset=0)',
             'def drums1():',
             '\treturn Notes(',
             '\t\ttimes      = (),',
             '\t\tkeys       = (),',
             '\t\tdurations  = (),',
             '\t\tvelocities = (),',
             ')')
    drums = '\n'.join(drums)

    bass = ('@track(channel="bass", font="default", bank=0, preset=0)',
            'def bass1():',
            '\treturn Notes(',
            '\t\ttimes      = (),',
            '\t\tkeys       = (),',
            '\t\tdurations  = (),',
            '\t\tvelocities = (),',
            ')')
    bass = '\n'.join(bass)

    sequence = ('@sequence()',
                'def main_sequence():',
                '\treturn {',
                '\t\t"drums":    (drums1),',
                '\t\t"bass":     (bass1),',
                '}')
    sequence = '\n'.join(sequence)

    player = ('@player(bpm=100, soundfont_path="../..", ticks_per_beat=96, start_part=1, end_part=0)',
              'def music():',
              '\treturn main_sequence')
    player = '\n'.join(player)

    return '\n\n'.join([file_name, channels, soundfonts, drums, bass, sequence, player, 'print("Success")'])

