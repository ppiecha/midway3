from __future__ import annotations
from collections.abc import Iterable, Callable
from enum import Enum
from functools import partial
from typing import NamedTuple, TYPE_CHECKING
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
type CombinationFunc = Callable[[], Iterable[NotesFunc]]
type VoiceRegistry = dict[str, VoiceArgs]
type VoiceCombinationRegistry = dict[str, CombinationFunc]


type UnitToTick = Callable[[float], Tick]


class Tick(int):
    def add(self, other):
        match other:
            case Tick():
                return Tick(self + int(other))
            case float() | int():  # TimeUnit
                return Tick(self + self.tick_from_unit(other))
            case _:
                raise TypeError(f"{type(other)} not supported")


class EventKind(str, Enum):
    NOTE = "note"
    PROGRAM = "program"
    CONTROL = "control"


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


type MidiEvents = Iterable[MidiEvent]


class MidiEventsWithTick(NamedTuple):
    tick: Tick
    midi_events: Iterable[MidiEvent]


class VoiceArgs(NamedTuple):
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
    music: Callable

    @property
    def tick_from_unit(self):
        return partial(unit2tick, bpm=self.bpm, ticks_per_beat=self.ticks_per_beat)
