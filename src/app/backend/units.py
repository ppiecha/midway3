# Converts unit: 1, 2, 4, 8... to tick
def unit2tick(unit: float, bpm: int, ticks_per_beat: int) -> int:
    if unit == 0:
        return 0
    beat_length = 60.0 / bpm
    second = beat_length * (4.0 / unit)
    return int(
        second2tick(
            second=second,
            ticks_per_beat=ticks_per_beat,
            tempo=bpm2tempo(bpm=bpm),
        )
    )


# Get ticks per second used in sequencer
def ticks_per_second(bpm: int, ticks_per_beat: int) -> int:
    return round(second2tick(second=1, ticks_per_beat=ticks_per_beat, tempo=bpm2tempo(bpm=bpm)))


def second2tick(second: float, ticks_per_beat: int, tempo: float) -> float:
    """Convert absolute time in seconds to ticks.

    Returns absolute time in ticks for a chosen MIDI file time
    resolution (ticks per beat, also called PPQN or pulses per quarter
    note) and tempo (microseconds per beat).
    """
    scale = tempo * 1e-6 / ticks_per_beat
    return second / scale


def bpm2tempo(bpm) -> int:
    """Convert beats per minute to MIDI file tempo.

    Returns microseconds per beat as an integer::

        240 => 250000
        120 => 500000
        60 => 1000000
    """
    # One minute is 60 million microseconds.
    return int(round((60 * 1000000) / bpm))
