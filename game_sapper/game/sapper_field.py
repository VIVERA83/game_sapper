from random import randint
from typing import Optional


class SapperField:
    _field: Optional[list[list[int]]] = None

    def __init__(self, height: int, width: int, count_mine: int):
        self._height = height
        self._width = width
        self._count_mine = count_mine
        self._create_field()

    def _create_field(self):
        self._field = [[0 for _ in range(self._width)] for _ in range(self._height)]
        for _ in range(self._count_mine):
            x, y = self._generate_coord_mine()
            self._barrier(x, y)

    def _generate_coord_mine(self) -> (int, int):
        while True:
            x = randint(0, self._width - 1)
            y = randint(0, self._height - 1)
            if self._field[y][x] >= 0:
                return x, y

    def _barrier(self, x: int, y: int):
        for y1 in range(-1, 2):
            for x1 in range(-1, 2):
                # Если координаты равны значит это мина вокруг которой строим барьер
                if (x == (x + x1)) and (y == (y + y1)):
                    self._field[y][x] = -1
                # Проверяем что бы координаты не выходили за границы
                elif 0 <= (y + y1) <= (self._height - 1) and 0 <= (x + x1) <= (self._width - 1):
                    if self._field[y + y1][x + x1] >= 0:
                        self._field[y + y1][x + x1] += 1

    def as_list(self):
        return self._field

    def as_str(self):
        return str(self._field)
