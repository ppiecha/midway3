from __future__ import annotations

from typing import NamedTuple, Callable, TYPE_CHECKING

from src.app.backend.types import (
    SoundfontIds,
    TrackRegistry,
    TrackMixRegistry,
    Channels,
    UnitToTick,
    PlayerArgs,
    Soundfonts,
    Tick,
    TrackChainRegistry,
)
from src.app.decorators.track_chain import TrackChain

if TYPE_CHECKING:
    from src.app.decorators.player import Player
    from src.app.decorators.track_mix import TrackMix
    from src.app.decorators.track import Track


class MusicArgs(NamedTuple):
    player: Player
    track: Track
    mix: TrackMix
    chain: TrackChain
    soundfont_ids: SoundfontIds | None

    def track_registry(self) -> TrackRegistry:
        return self.track.registry

    def track_args_by_name(self, name: str):
        return self.track_registry()[name]

    def mix_registry(self) -> TrackMixRegistry:
        return self.mix.registry

    def chain_registry(self) -> TrackChainRegistry:
        return self.chain.registry

    def channels(self) -> Channels:
        return self.track.channels_map_func()

    def soundfonts(self) -> Soundfonts:
        return self.track.soundfonts_map_func()

    def player_args(self) -> PlayerArgs:
        return self.player.args[0]

    def u2t(self) -> UnitToTick:
        return self.player_args().tick_from_unit

    def music_func(self) -> Callable:
        setattr(Tick, "tick_from_unit", self.player_args().tick_from_unit)
        return self.player_args().music_func
