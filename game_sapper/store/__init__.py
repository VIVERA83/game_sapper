import typing

from store.database.database import Database

if typing.TYPE_CHECKING:
    from core.app import Application


class Store:
    def __init__(self, app: "Application"):
        pass


def setup_store(app: "Application"):
    app.postgres = Database(app)
    app.store = Store(app)
