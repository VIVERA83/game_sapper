from aiohttp_apispec import docs, request_schema, response_schema

from core.componets import View
from core.utils import json_response

from game.schemas import (
    # UserIdRequestSchema,
    UserRequestSchema,
    UserSchema,
)


class UserAddView(View):
    @docs(
        tags=["user"],
        summary="Добавить нового игрока",
        description="Добавление игрока в игру ```Сапер```\n"
                    "Обратите внимание что ```vk_user_id``` не должен повторяться\n"
                    "Желательно заполнить ```username```",
    )
    @request_schema(UserRequestSchema)
    @response_schema(UserSchema)
    async def post(self):
        user = await self.store.sapper.create_user(self.data)
        self.logger.debug(f"{self.__class__.__name__} : {user}")
        return json_response(data=UserSchema().dump(user))


# class UserGetByVkIdViews(View):
#     @docs(
#         tags=[
#             "user",
#             "get",
#         ],
#         summary="Получить игрока по vk_id",
#         description="Получить данные по игроку ```Что? Где? Когда?```\n",
#     )
#     @querystring_schema(UserIdRequestSchema)
#     @response_schema(UserSchema)
#     async def get(self):
#         user = await self.store.game.get_user_by_vk_id(self.data.id)
#         self.logger.debug(f"{self.__class__.__name__} : {user}")
#         return json_response(
#             data=UserSchema().dump(user.as_dataclass if user else None)
#         )
