import json
import typing
from logging import getLogger

from store.vk_api.data_classes import Message, Update, TypeMessage, MessageFromVK, Payload, MessageToVK

if typing.TYPE_CHECKING:
    from core.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        self.bot = None
        self.logger = getLogger("handler")

    async def handle_updates(self, updates: list[Update]):
        if updates:
            for update in updates:
                #  TODO: Сюда нужно внести бота который обрабатывает сообщения
                #     и возвращает результат
                await self.app.store.vk_api.send_message(MessageToVK(
                    user_id=update.object.user_id,
                    text="Hello World, I tested",
                    keyboard=json.dumps({'one_time': False, 'buttons': [[{'action': {'type': 'text',
                                                                                     'label': 'Создать игру',
                                                                                     'payload': {'data': {},
                                                                                                 'keyboard_name': 'RootKeyboard',
                                                                                                 'button_name': 'Создать игру'}},
                                                                          'color': 'positive'}]]}),
                    type=TypeMessage.message_new,

                ))
