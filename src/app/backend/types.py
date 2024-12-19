from __future__ import annotations
from collections.abc import Iterable, Callable
from enum import Enum
from typing import NamedTuple

DEFAULT_VELOCITY = 100

type Time = float
type Key = int | None | tuple[int]
type Duration = int | None | tuple[int]
type Velocity = int | tuple[int]

type Tick = int
type Channel = int
type Channels = dict[str, int]
type Sequence = Iterable[Iterable[Callable[[], Notes]]]
type Tracks = dict[str, TrackArgs]

type UnitToTick = Callable[[float], int]


class EventKind(str, Enum):
    NOTE = "note"
    PROGRAM = "program"
    CONTROL = "control"


class Notes(NamedTuple):
    times: Iterable[Time]
    keys: Iterable[Key]
    durations: Iterable[Duration]
    velocities: Iterable[Velocity] | None = None
    programs: Iterable[Program | None] | None = None
    controls: Iterable[Control | None] | None = None


class Program(NamedTuple):
    bank: int
    preset: int


class Control(NamedTuple):
    control: int
    value: int


class Event(NamedTuple):
    time: Time
    key: Key
    duration: Duration
    velocity: Velocity
    program: Program | None = None
    control: Control | None = None


class MidiEvent(NamedTuple):
    kind: EventKind
    tick: Tick
    channel: Channel
    key: Key
    duration: Tick
    velocity: Velocity
    program: Program | None = None
    control: Control | None = None


class TrackArgs(NamedTuple):
    name: str
    channel_name: str
    notes: Callable
    bank: int = 0
    preset: int = 0


class PlayerArgs(NamedTuple):
    bpm: int
    soundfont_path: str
    soundfont: str
    ticks_per_beat: int
    sequences: Callable


class MusicArgs(NamedTuple):
    player: Callable[[int, str, int, int, int], Callable]
    track: Callable[[str, str, int, int], Callable]
    sequence: Callable[[], Callable]
