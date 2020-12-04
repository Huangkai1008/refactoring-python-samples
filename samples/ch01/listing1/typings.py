from dataclasses import dataclass
from typing import Dict, List, Literal

Genre = Literal['tragedy', 'comedy']
PlayID = Literal['hamlet', 'as-like', 'othello']


@dataclass(frozen=True)
class Play:
    name: str
    type: Genre


Plays = Dict[PlayID, Play]


@dataclass(frozen=True)
class Performance:
    play_id: PlayID
    audience: int


@dataclass(frozen=True)
class Invoice:
    customer: str
    performances: List[Performance]
