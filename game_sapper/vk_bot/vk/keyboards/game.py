from asyncio import Event, Lock

from vk_bot.data_classes import KeyboardEventEnum, MessageFromKeyboard, MessageFromVK
from vk_bot.vk.keyboards.data_classes import GameKeyboardSettings
from vk_bot.vk.vk_keyboard.buttons import Button
from vk_bot.vk.vk_keyboard.data_classes import TypeColor
from vk_bot.vk.vk_keyboard.keyboard import Keyboard as KeyboardSchema
from vk_bot.workers.keyboard import Keyboard
from game.sapper_field import SapperField
from icecream import ic


class GameKeyboard(Keyboard):
    name = "GameKeyboard"
    settings: GameKeyboardSettings

    def _init_(self):
        self.keyboard = KeyboardSchema(name=self.__class__.__name__, buttons={}, one_time=False)
        self.settings = GameKeyboardSettings(mine_field=SapperField(6, 5, 7).as_list())

    def create_buttons(self):
        """Создаем кнопки"""
        buttons = {}
        try:
            for y, row in enumerate(self.settings.mine_field):
                button_rows = []
                for x, column in enumerate(row):
                    button_rows.append(Button(
                        name=f"{x}:{y}",
                        label=f"❓",
                        color=TypeColor.white,
                    ))
                    self.button_handler[f"{x}:{y}"] = self.button_click
                buttons[y] = button_rows
            self.keyboard.buttons = buttons
        except Exception as e:
            self.logger.critical(e.args)

    async def button_click(self, message: MessageFromVK) -> "KeyboardEventEnum":
        x, y = map(int, message.payload.button_name.split(":"))
        if message.user_id not in self.settings.block:
            await self.click(message, x, y)
        else:
            message.body = f"{await self.bot.get_user_name(message.user_id)}: Душа сапера все ни как не упокоится"
        return KeyboardEventEnum.update

    async def click(self, message, x, y):
        """Проверяем: не занета ли клетка, что в клетке, бомба или все окей и
        делаем соответствующие действия с клавиатурой """
        if self.keyboard.buttons[y][x].color.value == TypeColor.white.value:
            if self.settings.mine_field[y][x] == -1:
                color = TypeColor.red
                label = "💣"
                message.body = f"{await self.bot.get_user_name(message.user_id)}: Пал Смертью храбрых"
                self.settings.block.append(message.user_id)
            else:
                color = TypeColor.green
                label = f"{self.settings.mine_field[y][x]}"
                message.body = f"{await self.bot.get_user_name(message.user_id)}: Разминировал еще одну ячейку"
            self.keyboard.buttons[y][x].color = color
            self.keyboard.buttons[y][x].label = label

    # async def event_new(self, message: MessageFromKeyboard) -> KeyboardEventEnum:
    #     await self.first_run_keyboard(message)
    #     return KeyboardEventEnum.update
    #
    # async def first_run_keyboard(self, message: MessageFromKeyboard):
    #     if not self.event.is_set():
    #         if self.users:
    #             self.event.set()
    #             self.settings = await self.get_setting_keyboard()
    #             self.create_buttons()
    #         else:
    #             self.logger.error(f"The list of users is empty: {self.users}")
    #
    # async def update(self):
    #     """Глобальное обновление клавиатуры"""
    #
    # async def button_click(self, message: MessageFromVK) -> "KeyboardEventEnum":
    #     x, y = map(int, message.payload.button_name.split(":"))
    #     if message.user_id not in self.settings.block:
    #         if self.keyboard.buttons[y][x].color.value == TypeColor.white.value:
    #             if self.settings.mine_field[y][x] == -1:
    #                 color = TypeColor.red
    #                 label = "💣"
    #                 message.body = f"{await self.bot.get_user_name(message.user_id)}: Пал Смертью храбрых"
    #                 self.settings.block.append(message.user_id)
    #             else:
    #                 color = TypeColor.green
    #                 label = self.settings.mine_field[y][x]
    #                 message.body = f"{await self.bot.get_user_name(message.user_id)}: Разминировал еще одну ячейку"
    #             self.keyboard.buttons[y][x].color = color
    #             self.keyboard.buttons[y][x].label = label
    #     else:
    #         message.body = f"{await self.bot.get_user_name(message.user_id)}: Душа сапера все ни как не упокоится"
    #     return KeyboardEventEnum.update
    #
    # async def get_keyboard_default_setting(self) -> GameKeyboardSettings:
    #     return GameKeyboardSettings(mine_field=SapperField(6, 5, 7).as_list())
