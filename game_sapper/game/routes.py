import typing

if typing.TYPE_CHECKING:
    from core.app import Application


def setup_routes(app: "Application"):
    from game.views import UserAddView

    app.router.add_view("/add_user", UserAddView)
