from typing import TYPE_CHECKING, Type, Union
from dataclasses import dataclass, asdict, field

from icecream import ic

if TYPE_CHECKING:
    from bot.workers.keyboard import Keyboard


@dataclass
class BaseDataClass:
    @property
    def as_dict(self) -> dict:
        return asdict(self)


@dataclass()
class Data:
    value: Union[int, str, bool, dict]
    row: int
    button_name: str


@dataclass
class TimeoutKeyboard:
    keyboard: Type["Keyboard"]
    user_ids: list[int]
    keyboards: list[str] = None
    is_dynamic: bool = False
    is_private: bool = False
    body: str = "Переход в связи с окончанием времени"
    settings: "GameSessionSettings" = (None,)

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class GameSessionSettings(BaseDataClass):
    players: "Data"
    rounds: "Data"
    id: int = None

    @property
    def get_rows(self) -> dict[str, int]:
        return {
            self.rounds.button_name: self.rounds.row,
            self.players.button_name: self.players.row,
        }


@dataclass
class TeamIsReady(BaseDataClass):
    buttons: dict[str, Union[bool, "Data"]] = field(default_factory=dict)

    def init(self, users: list[int]) -> "TeamIsReady":
        ic(users)
        for user_id in users:
            self.buttons[f"{user_id}_"] = False
        return self

    @property
    def get_rows(self) -> dict[str, bool]:
        return {button_name: row for button_name, row in self.buttons}


@dataclass
class Round:
    number: int
    answer: str = None
    users: dict[str, "Data"] = field(default_factory=dict)
    answers: dict[str, "Data"] = field(default_factory=dict)
    votes: dict[str, "Data"] = field(default_factory=dict)


