from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Optional


class TypeMessage(Enum):
    message_new = "message_new"
    message_event = "message_event"
    message_reply = "message_reply"
    message_edit = "message_edit"


@dataclass
class Payload:
    keyboard_name: Optional[str] = None
    button_name: Optional[str] = None

    @property
    def as_dict(self):
        return asdict(self)


@dataclass
class Message:
    id: int
    text: str
    payload: Payload  # noqa
    peer_id: int
    user_id: int


@dataclass
class EventMessage:
    event_id: str
    user_id: int
    peer_id: int
    event_data: str = None
    keyboard: str = None


@dataclass
class Object:
    message: Message


@dataclass
class Update:
    type: TypeMessage
    object: Object

    event_id: str
    group_id: int
    object: Object
    type: TypeMessage
    v: str

    def as_dict(self):
        return {"object": asdict(self.object), "type": self.type.value}


@dataclass
class VKResponse:
    ts: int = 0
    updates: list[Update] = field(default_factory=list)
    failed: int = None
    error: dict = None

    def as_dict(self):
        return asdict(self)


@dataclass
class MessageToVK:
    user_id: int
    text: str
    keyboard: str

    type: TypeMessage
    event_id: str = None
    peer_id: int = None
    event_data: str = "Test Schema BOT"
