import typing
from asyncio import Queue
from base.base_accessor import BaseAccessor
from store.manager.poller import Poller
from vk_bot.data_classes import MessageFromVK
from vk_bot.vk.keyboards.root import RootKeyboard
from vk_bot.workers.dispatcher import Bot
from store.vk_api.data_classes import Update

if typing.TYPE_CHECKING:
    from core.app import Application


class BotManager(BaseAccessor):
    poller: typing.Optional[Poller] = None

    def _init_(self, app: "Application", *_: list, **__: dict):
        self.app = app
        self.vk_bot = Bot(
            app=app,
            user_expired=app.settings.bot.user_expired,
            keyboard_expired=app.settings.bot.keyboard_expired,
            root_keyboard=RootKeyboard,
            name=app.settings.bot.name,
            queue_input=Queue(),
            queue_output=Queue(),
            logger=app.logger,
        )

        self.logger = app.logger

    async def connect(self, app: "Application"):
        self.poller = Poller(app.store)
        await self.vk_bot.start()
        await self.poller.start()
        self.logger.info("Started BotManager")

    async def disconnect(self, app: "Application"):
        await self.vk_bot.stop()
        await self.poller.stop()
        self.logger.info("Stopped BotManager")

    async def handle_updates(self, updates: list[Update]):
        for update in updates:
            await self.vk_bot.queue_input.put(MessageFromVK(
                user_id=update.object.message.user_id,
                body=update.object.message.text,
                type=update.type,
                payload=update.object.message.payload,
                event_id=update.event_id,
                peer_id=update.object.message.peer_id,
            ))
