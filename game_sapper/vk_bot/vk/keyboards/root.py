from vk_bot.data_classes import KeyboardEventEnum, MessageFromVK
from vk_bot.vk.vk_keyboard.buttons import Button, Title
from vk_bot.vk.vk_keyboard.data_classes import TypeColor
from vk_bot.vk.vk_keyboard.keyboard import Keyboard as KeyboardSchema
from vk_bot.workers.keyboard import Keyboard

base_structure = {
    0: [
        Title(
            name="Сапер",
            label="Сапер",
            color=TypeColor.white,
            help_string="Классическая игра реализованная в боте"
        )
    ],
    1: [

        Button(
            name="Одиночная игра",
            label="Одиночная игра",
            color=TypeColor.blue,
        ),
        Button(
            name="Игра против игрока",
            label="Игра против игрока",
            color=TypeColor.blue,
        ),
    ],
    2: [
        Button(
            name="Присоединится",
            label="Присоединится",
            color=TypeColor.blue,
        ),
        Button(
            name="Продолжить",
            label="Продолжить",
            color=TypeColor.blue,
        )

    ],
    3: [
        Button(
            name="О проекте",
            label="О проекте",
            color=TypeColor.white,
        )
    ]
}


class RootKeyboard(Keyboard):
    name = "RootKeyboard"

    def _init_(self):
        self.keyboard = KeyboardSchema(name=self.__class__.__name__, buttons=base_structure, one_time=False)
        self.button_handler = {
            "Одиночная игра": self.button_greate_game,
            "Продолжить": self.button_continue_game,
            "Присоединится": self.button_join_game,
            "О проекте": self.button_about,
        }

    async def button_greate_game(self, message: "MessageFromVK") -> "KeyboardEventEnum":
        from vk_bot.vk.keyboards.game_config import GameConfigKeyboard
        return await self.redirect(
            keyboard=GameConfigKeyboard,
            user_ids=[message.user_id],
            is_private=True,

        )

    async def button_continue_game(self, message: "MessageFromVK") -> "KeyboardEventEnum":
        """Переход в меню выбора игры для продолжения"""
        message.body = "Пока возможность продолжать прерванные игры ранее, нет... но скоро будет!"
        return KeyboardEventEnum.select

    async def button_join_game(self, message: "MessageFromVK") -> "KeyboardEventEnum":
        """Переход в меню выбора готовых игр ожидающих партнеров"""
        message.body = "Пока возможность присоединится к игре не реализована... но скоро будет!"
        return KeyboardEventEnum.select

    async def button_about(self, message: "MessageFromVK") -> "KeyboardEventEnum":
        """Описание проекта"""
        message.body = "Пет проект, подробная информация на https://github.com/VIVERA83/KTS_WINTER_2023_4_XO"
        return KeyboardEventEnum.select
