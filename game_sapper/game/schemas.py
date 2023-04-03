from typing import Optional, Union
from game.data_classes import (

    Round,
    User, UserRequest, GameSession,
)
from marshmallow import (
    EXCLUDE,
    Schema,
    ValidationError,
    fields,
    post_load,

)

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

    vk_user_id = fields.Int(required=True, validate=lambda data: validate_vk_user_id(data), example="1")
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


def validate_vk_user_id(data: int):
    if data < 1:
        raise ValidationError("The value must be greater than 0")
