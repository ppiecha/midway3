from __future__ import annotations

import typing
from collections.abc import Iterable
from typing import NamedTuple

from src.app.backend.types import (
    SoundfontIds,
    VoiceRegistry,
    VoiceMixRegistry,
    Channels,
    UnitToTick,
    PlayerArgs,
    Soundfonts,
    Tick,
    NotesFunc,
)

if typing.TYPE_CHECKING:
    from src.app.decorators.player import Player
    from src.app.decorators.voice_mix import VoiceMix
    from src.app.decorators.voice import Voice


class MusicArgs(NamedTuple):
    player: Player
    voice: Voice
    mix: VoiceMix
    soundfont_ids: SoundfontIds | None

    def voice_registry(self) -> VoiceRegistry:
        return self.voice.registry

    def voice_args_by_name(self, name: str):
        return self.voice_registry()[name]

    def voice_combinations(self) -> VoiceMixRegistry:
        return self.mix.registry

    def channels(self) -> Channels:
        return self.voice.channels_map_func()

    def soundfonts(self) -> Soundfonts:
        return self.voice.soundfonts_map_func()

    def player_args(self) -> PlayerArgs:
        return self.player.args[0]

    def u2t(self) -> UnitToTick:
        return self.player_args().tick_from_unit

    def music(self) -> Iterable[NotesFunc]:
        setattr(Tick, "tick_from_unit", self.player_args().tick_from_unit)
        msc = self.player_args().music()
        if isinstance(msc, Iterable):
            raise TypeError("Iterable not supported yet")
        return msc()
