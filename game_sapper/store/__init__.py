import typing

from store.database.database import Database
from store.game.accessor import GameAccessor

if typing.TYPE_CHECKING:
    from core.app import Application


class Store:
    def __init__(self, app: "Application"):
        self.sapper = GameAccessor(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.store = Store(app)
