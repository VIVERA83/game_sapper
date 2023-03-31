from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.models import GameSessionModel, RoundModel


@dataclass
class BaseDataClass:
    @property
    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class User(BaseDataClass):
    id: int
    vk_user_id: int
    username: str
    game_sessions: list["GameSessionModel"]
    rounds: list["RoundModel"]


@dataclass
class GameSession(BaseDataClass):
    id: int
    field: str
    users: list["User"]
    rounds: list["Round"]


@dataclass
class Round(BaseDataClass):
    id: int
    game_session_id: int
    round_number: int
    player_id: int
    cords: str
    result: str
