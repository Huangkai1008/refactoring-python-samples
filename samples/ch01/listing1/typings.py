from dataclasses import dataclass
from typing import Dict, List, Literal

Genre = Literal['tragedy', 'comedy']
PlayID = Literal['hamlet', 'as-like', 'othello']


@dataclass
class Play:
    name: str
    type: Genre


Plays = Dict[PlayID, Play]


@dataclass
class Performance:
    play_id: PlayID
    audience: int


@dataclass
class Invoice:
    customer: str
    performances: List[Performance]
