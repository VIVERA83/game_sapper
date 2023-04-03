from typing import TYPE_CHECKING, Type, Union
from dataclasses import dataclass, asdict, field

if TYPE_CHECKING:
    from vk_bot.workers.keyboard import Keyboard


@dataclass
class BaseDataClass:
    @property
    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class TimeoutKeyboard:
    keyboard: Type["Keyboard"]
    user_ids: list[int]
    keyboards: list[str] = None
    is_dynamic: bool = False
    is_private: bool = False
    body: str = "Переход в связи с окончанием времени"

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Data:
    value: Union[int, str, bool, dict]
    row: int
    button_name: str


@dataclass
class GameConfigSettings:
    mines: Data
    cell: Data

    @property
    def get_rows(self) -> dict[str, int]:
        return {
            self.cell.button_name: self.cell.row,
            self.mines.button_name: self.mines.row,
        }


@dataclass
class GameSettings:
    mine_field: list[list[int]] = field(default_factory=list)
    block: list[int] = field(default_factory=list)
