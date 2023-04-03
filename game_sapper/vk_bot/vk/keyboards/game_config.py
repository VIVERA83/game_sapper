from typing import Optional

from vk_bot.data_classes import KeyboardEventEnum, MessageFromVK
from vk_bot.vk.keyboards.data_classes import GameConfigSettings, Data, GameSettings
from vk_bot.vk.vk_keyboard.buttons import Button, Title
from vk_bot.vk.vk_keyboard.data_classes import TypeColor
from vk_bot.vk.vk_keyboard.keyboard import Keyboard as KeyboardSchema
from vk_bot.workers.keyboard import Keyboard
from game.sapper_field import SapperField

base_structure = {
    0: [
        Title(
            name="Настройка",
            label="Настройка",
            color=TypeColor.white,
            help_string="Здесь вы можете настроить игру, выбрать количество мин и другие настройки",
        )
    ],
    1: [
        Title(
            name="Количество мин",
            label="Количество мин",
            color=TypeColor.white,
            help_string="Чем больше мин тем сложней играть",
        )
    ],
    2: [
        Button(
            name="5 mines",
            label="5",
            color=TypeColor.blue,
        ),
        Button(
            name="7 mines",
            label="7",
            color=TypeColor.blue,
        ),
        Button(
            name="10 mines",
            label="10",
            color=TypeColor.blue,
        ),
    ],
    3: [
        Title(
            name="Размер поля",
            label="Размер поля",
            color=TypeColor.white,
            help_string="Размер поля  которое нужно будет разминировать, кол-во ячеек",
        )
    ],
    4: [
        Button(
            name="25 cell",
            label="25",
            color=TypeColor.blue,
        ),
        Button(
            name="30 cell",
            label="30",
            color=TypeColor.blue,
        ),
        Button(
            name="35 cell",
            label="35",
            color=TypeColor.blue,
        ),
    ],
    5: [
        Button(
            name="Создать",
            label="Создать",
            color=TypeColor.green,
        ),
        Button(
            name="Назад",
            label="Назад",
            color=TypeColor.red,
        ),
    ],
}


class GameConfigKeyboard(Keyboard):
    name = "GameConfigKeyboard"
    settings: Optional["GameConfigSettings"] = None

    def _init_(self):
        self.keyboard = KeyboardSchema(name=self.__class__.__name__, buttons=base_structure, one_time=False)
        self.button_handler = {
            "5 mines": lambda message: self.button_update_players(message, 5),
            "7 mines": lambda message: self.button_update_players(message, 7),
            "10 mines": lambda message: self.button_update_players(message, 10),
            "25 cell": lambda message: self.button_update_field_size(message, 25),
            "30 cell": lambda message: self.button_update_field_size(message, 30),
            "35 cell": lambda message: self.button_update_field_size(message, 35),
            "Создать": self.button_greate_game,
            "Назад": self.button_back,
        }
        self.settings = GameConfigSettings(mines=Data(5, 2, "5 mines"),
                                           cell=Data(25, 4, "25 cell"))

    async def update(self):
        self.change_color()

    def change_color(self, ):
        """Меняем цвет кнопки, в колонке, а остальным назначаем другой цвет"""
        for button_name, row in self.settings.get_rows.items():
            buttons = self.keyboard.buttons.get(row)
            for button in buttons:
                if button.name == button_name:
                    button.color = TypeColor.green
                else:
                    button.color = TypeColor.blue

    async def button_update_players(self, message: MessageFromVK, value: int) -> "KeyboardEventEnum":
        """Изменение количества мин на игровом поле"""
        # Назначаем новое значение в настройках и в клавиатуре
        self.settings.mines.value = value
        self.settings.mines.button_name = message.payload.button_name
        message.body = f"Изменен размер команды, теперь {value}"
        return KeyboardEventEnum.select

    async def button_update_field_size(self, message: MessageFromVK, value: int) -> "KeyboardEventEnum":
        """Изменение размера игрового поля"""
        # Назначаем новое значение в настройках и в клавиатуре
        self.settings.cell.value = value
        self.settings.cell.button_name = message.payload.button_name
        message.body = f"Изменено количество раундов в игре на {value}"
        return KeyboardEventEnum.select

    async def button_greate_game(self, message: "MessageFromVK") -> "KeyboardEventEnum":
        from vk_bot.vk.keyboards.game import GameKeyboard
        height = self.settings.cell.value // 5
        return await self.redirect(
            keyboard=GameKeyboard,
            user_ids=[message.user_id],
            is_private=True,
            settings=GameSettings(
                mine_field=SapperField(height=height,
                                       width=5,
                                       count_mine=self.settings.mines.value).as_list()
            )
        )

    async def button_back(self, message: MessageFromVK) -> "KeyboardEventEnum":
        """Вернуться в главное меню"""
        from vk_bot.vk.keyboards.root import RootKeyboard
        return await self.redirect(RootKeyboard, [message.user_id],
                                   body=f"{self.get_user(message.user_id).name} : Перешел в Основное меню")
