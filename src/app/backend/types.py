from __future__ import annotations
from collections.abc import Iterable, Callable
from enum import Enum
from functools import partial
from typing import NamedTuple, Generator
from src.app.backend.units import unit2tick

DEFAULT = "default"
DEFAULT_VELOCITY = 100

type TimeUnit = float
type Key = int | None | tuple[int]
type Duration = int | None | tuple[int]
type Velocity = int | tuple[int]
type Channel = int
type Channels = dict[str, int]
type ChannelsMapFunc = Callable[[], Channels]
type Soundfonts = dict[str, str]
type SoundfontsMapFunc = Callable[[], Soundfonts]
type SoundfontIds = dict[str, int]
type NotesFunc = Callable[[], Notes]
type Funcs = NotesFunc | MixFunc | ChainFunc
type MixFunc = Callable[[], Iterable[Funcs]]
type ChainFunc = Callable[[], Iterable[Funcs]]
type TrackRegistry = dict[str, TrackArgs]
type TrackMixRegistry = dict[str, MixFunc]
type TrackChainRegistry = dict[str, ChainFuncFunc]


type UnitToTick = Callable[[float], Tick]


class Tick(int):
    def add(self, other):
        match other:
            case Tick():
                return Tick(self + int(other))
            case float() | int():
                return Tick(self + self.tick_from_unit(other))
            case _:
                raise TypeError(f"{type(other)} not supported")


class EventKind(str, Enum):
    NOTE = "note"
    PROGRAM = "program"
    CONTROL = "control"
    META_END_OF_BAR = "meta_end_of_bar"
    META_END_OF_USER_SEQ = "meta_end_of_user_seq"


class FunctionType(str, Enum):
    TRACK = "track"
    MIX = "mix"
    CHAIN = "chain"


class Notes(NamedTuple):
    times: Iterable[TimeUnit]
    keys: Iterable[Key] | None = None
    durations: Iterable[Duration] | None = None
    velocities: Iterable[Velocity] | None = None
    programs: Iterable[Program | None] | None = None
    controls: Iterable[Control | None] | None = None


class Program(NamedTuple):
    sfid: int
    bank: int
    preset: int


class Control(NamedTuple):
    control: int
    value: int


class Event(NamedTuple):
    time: TimeUnit
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
    duration: Tick | None
    velocity: Velocity | None
    program: Program | None = None
    control: Control | None = None


type Gen[T] = Generator[T, None, None]


class MidiEventsWithTick(NamedTuple):
    tick: Tick
    midi_events: Iterable[MidiEvent]


class TrackArgs(NamedTuple):
    name: str
    channel_name: str
    notes_fn: NotesFunc
    soundfont: str
    bank: int = 0
    preset: int = 0


class PlayerArgs(NamedTuple):
    bpm: int
    soundfont_path: str
    soundfont: str
    ticks_per_beat: int
    music_func: Callable

    @property
    def tick_from_unit(self):
        return partial(unit2tick, bpm=self.bpm, ticks_per_beat=self.ticks_per_beat)
