from vk_bot.data_classes import KeyboardEventEnum, MessageFromVK
from vk_bot.vk.vk_keyboard.buttons import Button
from vk_bot.vk.vk_keyboard.data_classes import TypeColor
from vk_bot.vk.vk_keyboard.keyboard import Keyboard as KeyboardSchema
from vk_bot.workers.keyboard import Keyboard

base_structure = {
    0: [
        Button(
            name="Играть",
            label="Играть",
            color=TypeColor.white,
        )
    ],
}


class RootKeyboard(Keyboard):
    name = "RootKeyboard"

    def _init_(self):
        self.keyboard = KeyboardSchema(name=self.__class__.__name__, buttons=base_structure, one_time=False)
        self.button_handler = {
                 "Играть": self.button_greate_game,
             }

    async def button_greate_game(self, message: "MessageFromVK") -> "KeyboardEventEnum":
        from vk_bot.vk.keyboards.game import GameKeyboard
        return await self.redirect(
            keyboard=GameKeyboard,
            user_ids=[message.user_id],
            is_private=True,
        )

