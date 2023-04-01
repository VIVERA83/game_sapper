import json
from dataclasses import dataclass
from typing import Optional, Type, Union

from marshmallow import EXCLUDE, Schema, fields, post_load, pre_load
from marshmallow_enum import EnumField

from store.vk_api.data_classes import (
    EventMessage,
    Message,
    Object,
    Payload,
    TypeMessage,
    Update,
    VKResponse,
)


objects = Union[
    Type[VKResponse],
    Type[Update],
    Type[Update],
    Type[Payload],
    Type[Message],
    Type[EventMessage],
]


class BaseSchema(Schema):
    __model__: Optional[dataclass] = None

    @post_load
    def make_object(self, data, **_: dict) -> objects:
        return self.__model__(**data)

    class Meta:
        unknown = EXCLUDE
        ordered = True


class MessageSchema(BaseSchema):
    __model__ = Message

    id = fields.Int()
    user_id = fields.Integer()
    text = fields.String()
    payload = fields.Nested("PayloadSchema", load_default=Payload())  # noqa
    peer_id = fields.Int()

    @pre_load
    def make_obj(self, value: Union[str, dict], **_: dict):
        if not value.get("user_id"):
            value["user_id"] = value.get("from_id")
        if isinstance(value.get("payload"), str):
            value["payload"] = json.loads(value.get("payload"))
            if not value["payload"].get("data"):
                value["payload"]["data"] = {}
            return value
        return value


class PayloadSchema(BaseSchema):
    __model__ = Payload

    keyboard_name = fields.Str()
    button_name = fields.Str()


class ObjectSchema(BaseSchema):
    __model__ = Object

    message = fields.Nested(MessageSchema())

    @pre_load
    def make_obj(self, value: Union[str, dict], **_: dict):
        if value.get("user_id"):
            value["message"] = {
                "id": 0,
                "text": "Test",
                "user_id": value["user_id"],
                "payload": value["payload"],
                "peer_id": value["peer_id"],
            }
            return value
        return value


class UpdateSchema(BaseSchema):
    __model__ = Update

    event_id = fields.Str()
    group_id = fields.Int()
    object = fields.Nested(ObjectSchema())
    type = EnumField(TypeMessage)
    v = fields.Str()

    @pre_load
    def make_obj(self, value: Union[str, dict], **_: dict):
        if value.get("type") == TypeMessage.message_event.value:
            value["event_id"] = value.get("object")["event_id"]
        return value


class VKResponseSchema(BaseSchema):
    __model__ = VKResponse

    ts = fields.Integer()
    failed = fields.Int()
    updates = fields.List(fields.Nested(UpdateSchema()), load_default=None)
    error = fields.Dict(load_default=None)
