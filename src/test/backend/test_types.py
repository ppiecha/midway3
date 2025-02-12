from functools import partial

from src.app.backend.types import Tick
from src.app.backend.units import unit2tick

fn = partial(unit2tick, bpm=60, ticks_per_beat=96)
setattr(Tick, "tick_from_unit", fn)


def test_tick_int():
    assert Tick(1).add(2) == 193


def test_tick_float():
    assert Tick(1).add(2.0) == 193


def test_tick_tick():
    assert Tick(1).add(Tick(2)) == 3


def test_tick():
    assert Tick(96).add(4) == 192
