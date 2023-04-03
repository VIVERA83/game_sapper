from typing import Optional

from vk_bot.data_classes import KeyboardEventEnum, MessageFromVK
from vk_bot.vk.keyboards.data_classes import GameSettings
from vk_bot.vk.keyboards.root import RootKeyboard
from vk_bot.vk.vk_keyboard.buttons import Button
from vk_bot.vk.vk_keyboard.data_classes import TypeColor
from vk_bot.vk.vk_keyboard.keyboard import Keyboard as KeyboardSchema
from vk_bot.workers.keyboard import Keyboard


class GameKeyboard(Keyboard):
    name = "GameKeyboard"
    settings: Optional["GameSettings"] = None

    def _init_(self):
        self.keyboard = KeyboardSchema(name=self.__class__.__name__, buttons={}, one_time=False)

    def create_buttons(self):
        """Создаем кнопки"""
        buttons = {}

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
        self.keyboard.buttons.update({len(self.keyboard.buttons): [Button(
            name="Покинуть игру",
            label="Покинуть игру",
            color=TypeColor.white,
        )]})
        self.button_handler["Покинуть игру"] = self.button_quit

    async def button_click(self, message: MessageFromVK) -> "KeyboardEventEnum":
        x, y = map(int, message.payload.button_name.split(":"))
        if message.user_id not in self.settings.block:
            await self.click(message, x, y)
        else:
            message.body = f"{await self.bot.get_user_name(message.user_id)}: Душа сапера все ни как не упокоится"
        return KeyboardEventEnum.update

    async def button_quit(self, message: MessageFromVK) -> KeyboardEventEnum:
        # обнуляем настройки по клавиатуре, иначе они будут всплывать при новой игре
        self.get_user(message.user_id).set_setting_keyboard(self.__class__.__name__, None)
        return await self.redirect(RootKeyboard, [message.user_id], kill_parent=True)

    async def click(self, message, x, y):
        """Проверяем: не занята ли клетка, что в клетке, бомба или все окей и
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
