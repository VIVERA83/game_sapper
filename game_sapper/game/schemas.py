from typing import Optional, Union

from game.data_classes import (
    # GameSession,
    Round,
    User, UserRequest, GameSession,
)
from marshmallow import (
    EXCLUDE,
    Schema,
    # ValidationError,
    fields,
    post_load,
    # pre_dump,
    # validates,
    # validates_schema,
)

# from marshmallow.validate import OneOf

game_objects = Union[Round, User]


class BaseSchema(Schema):
    __model__ = Optional[game_objects]

    @post_load
    def make_object(self, data: dict, **_: dict) -> game_objects:
        return self.__model__(**data)

    class Meta:
        ordered = True
        unknown = EXCLUDE


class UserSchema(BaseSchema):
    __model__ = User

    id = fields.Int(required=True, example=1)
    vk_user_id = fields.Int(required=True, example="1")
    username = fields.Str(example="Павел Дуров")
    game_sessions = fields.Nested("GameSessionSchema", many=True)  # noqa
    rounds = fields.Nested("RoundSchema", many=True)  # noqa


class UserRequestSchema(BaseSchema):
    __model__ = UserRequest

    vk_user_id = fields.Int(required=True, example="1")
    username = fields.Str(example="Павел Дуров")


class GameSessionSchema(BaseSchema):
    __model__ = GameSession

    id = fields.Int(required=True, example=1)
    field = fields.Str(required=True, example="НУЖНО ПРИДУМАТЬ")
    users = fields.Nested("UserSchema", many=True)  # noqa
    rounds = fields.Nested("RoundSchema", many=True)  # noqa


class RoundSchema(BaseSchema):
    __model__ = Round

    id = fields.Int(required=True, example="1")
    game_session_id = fields.Int(required=True, example=1)
    round_number = fields.Int(required=True, example=1)
    player_id = fields.Int(required=True, example=3254876)
    cords = fields.Str(required=True, example="НУЖНО ПРИДУМАТЬ")
    result = fields.Str(required=True, example="НУЖНО ПРИДУМАТЬ")

#
#
# class RoundRequestSchema(BaseSchema):
#     __model__ = RoundRequest
#     respondent_id = fields.Int(required=True, example=1)
#     answer = fields.Str(required=True, example="Hello World")
#     question_id = fields.Int(required=True, example=1)
#     game_session_id = fields.Int(required=True, example=1)


# class GameSessionRequestSchema(BaseSchema):
#     __model__ = GameSessionRequest
#
#     captain_id = fields.Int(required=True, example=1)
#     users = fields.List(fields.Int(), required=True, example=[1, 2, 3])
#
#     @validates("users")
#     def validate_users(self, value):
#         if len(set(value)) != len(value):
#             raise ValidationError("No repetition")
#         for index, user in enumerate(value):
#             if user < 1:
#                 raise ValidationError(f"users[{index}] must be greater than 0.")
#
#     @validates_schema
#     def validate_captain_id(self, data, **__: dict):
#         OneOf(
#             data["users"],
#             error=f"`captain_id`{data['captain_id']} should be in the `users` list {data['users']}",
#         )(data["captain_id"])
#         if data["captain_id"] != data["users"][0]:
#             raise ValidationError(
#                 f"The `captain_id` {data['captain_id']} must be the first"
#             )
#

# class UserIdRequestSchema(BaseSchema):
#     __model__ = UserIdRequest
#     id = fields.Int(required=True, example=1)
#
#
