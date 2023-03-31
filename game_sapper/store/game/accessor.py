from base.base_accessor import BaseAccessor
from game.sapper_field import SapperField


class GameAccessor(BaseAccessor):
    def create_game(self, users: list[int], count_mine: int):
        """Создается игровая сессия"""
        field = SapperField(5, 8, 10).as_str()
        