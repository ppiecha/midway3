import os
from typing import Callable

from src.app.utils.file_ops import write_file
from src.app.utils.logger import get_console_logger

logger = get_console_logger(__name__)


def new_file(file_name: str, path: str = "", file_content_fn: Callable | None = None):
    full_path = os.path.join(path, file_name)
    logger.debug(f"{full_path = }")
    write_file(full_path=full_path, content=file_content_fn(file_name))


def file_content(file_name: str) -> str:
    file_name = f"# {file_name}"
    imports = f"from itertools import count"

    channels = (
        "@voice.channels",
        "def channels_map():",
        "\treturn {",
        '\t\t"drums":    10,',
        '\t\t"bass":     0,',
        '\t\t"piano":    1,',
        "}",
    )
    channels = "\n".join(channels)

    soundfonts = ("@voice.soundfonts", "def soundfonts_map():", "\treturn {", '\t\t"default": "soundfont.sf2",', "}")
    soundfonts = "\n".join(soundfonts)

    drums = (
        '@voice(channel="drums", soundfont = "default", bank=128, preset=0)',
        "def drums1():",
        "\treturn Notes(",
        "\t\ttimes      = (8 ,) * 8,",
        "\t\tkeys       = (37,) * 8,",
        "\t\tdurations  = (32,) * 8,",
        "\t\t#velocities = (),",
        ")",
    )
    drums = "\n".join(drums)

    bass = (
        '@voice(channel="bass", soundfont = "default", bank=0, preset=24)',
        "def bass1():",
        "\treturn Notes(",
        "\t\ttimes      = (4 ,) * 4,",
        "\t\tkeys       = (60, 59, 57, 55),",
        "\t\tdurations  = (8,) * 4,",
        "\t\t#velocities = (),",
        ")",
    )
    bass = "\n".join(bass)

    piano = (
        '@voice(channel="piano", soundfont = "default", bank=0, preset=0)',
        "def piano1():",
        "\treturn Notes(",
        "\t\ttimes      = (4 ,) * 4,",
        "\t\tkeys       = (72, 74, 76, 77),",
        "\t\tdurations  = (8,) * 4,",
        "\t\t#velocities = (),",
        ")",
    )
    piano = "\n".join(piano)

    sequence1 = (
        "@cmb()",
        "def cmb1():",
        "\treturn drums1, bass1",
    )
    sequence1 = "\n".join(sequence1)

    # sequence2 = (
    #     "@sequence()",
    #     "def sequence2():",
    #     "\treturn [",
    #     "\t\t(drums1, piano1),",
    #     "\t\t(drums1, bass1),",
    #     "\t]",
    # )
    # sequence2 = "\n".join(sequence2)

    player = (
        '@player(bpm=60, soundfont_path="../..", soundfont="soundfont.sf2", ticks_per_beat=96, start_part=1, end_part=0)',
        "def music():",
        "\treturn cmb1 ",
    )
    player = "\n".join(player)

    return "\n\n".join(
        [file_name, imports, channels, soundfonts, drums, bass, piano, sequence1, player, 'print("Success")']
    )
