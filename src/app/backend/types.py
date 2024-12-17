from typing import Tuple, NamedTuple, Iterable


DEFAULT_VELOCITY = 100

type Time = float
type Key = int | None | Tuple[int]
type Duration = int | None | Tuple[int]
type Velocity = int | Tuple[int]


class Notes(NamedTuple):
    times: Iterable[Time]
    keys: Iterable[Key]
    durations: Iterable[Duration]
    velocities: Iterable[Velocity] | None = None


class Event(NamedTuple):
    time: Time
    key: Key
    duration: Duration
    velocity: Velocity
