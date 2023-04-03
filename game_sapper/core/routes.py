import typing

if typing.TYPE_CHECKING:
    from core.componets import Application


def setup_routes(app: "Application"):
    from game.routes import setup_routes as game_setup_routes

    game_setup_routes(app)
