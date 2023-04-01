import typing

from store.database.database import Database

if typing.TYPE_CHECKING:
    from core.app import Application


class Store:
    def __init__(self, app: "Application"):
        from store.game.accessor import GameAccessor
        from store.vk_api.accessor import VkApiAccessor
        from store.bot.manager import BotManager

        self.sapper = GameAccessor(app)
        self.vk_api = VkApiAccessor(app)
        self.bots_manager = BotManager(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.store = Store(app)
