import asyncio
import json
import random
import traceback
from typing import Optional, TYPE_CHECKING

from aiohttp import TCPConnector
from aiohttp.client import ClientSession

from base.base_accessor import BaseAccessor
from store.vk_api.data_classes import EventMessage, Update, VKResponse, MessageToVK
from store.vk_api.poller import Poller
from store.vk_api.schemes import VKResponseSchema

if TYPE_CHECKING:
    from core.app import Application

API_PATH = "https://api.vk.com/method/"


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.poller: Optional[Poller] = None
        self.ts: Optional[int] = None

    async def connect(self, app: "Application"):
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        try:
            await self._set_long_poll_service()
            await self._get_long_poll_service()
        except Exception as e:  # плохо
            # traceback.format_exc() if request.app.settings.traceback else error
            self.logger.error(traceback.format_exc() if self.app.settings.traceback else f"Exception: {e.args}")
        self.poller = Poller(app.store)
        await self.poller.start()
        self.logger.info("start polling")

    async def disconnect(self, app: "Application"):
        if self.poller and self.poller.is_running:
            await self.poller.stop()
        if self.session and not self.session.closed:
            await self.session.close()
            # нужно, что бы корректно закрылся VKApiAccessor. Иначе вылетает ошибка "Event loop is closed"
        await asyncio.sleep(0.1)
        self.app.logger.info("VkApiAccessor disconnecting is complete")

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _set_long_poll_service(self):
        async with self.session.get(
                self._build_query(
                    host=API_PATH,
                    method="groups.setLongPollSettings",
                    params={
                        "group_id": self.app.settings.vk.group_id,
                        "access_token": self.app.settings.vk.token,
                        "message_reply": 0,
                    },
                )
        ) as resp:
            data = await resp.json()
            vk_response: VKResponse = VKResponseSchema().load(data)
            if vk_response.error:
                self.logger.critical(f"{vk_response.error}")
                return

    async def _get_long_poll_service(self):
        async with self.session.get(
                self._build_query(
                    host=API_PATH,
                    method="groups.getLongPollServer",
                    params={
                        "group_id": self.app.settings.vk.group_id,
                        "access_token": self.app.settings.vk.token,
                    },
                )
        ) as resp:
            data = await resp.json()
            vk_response: VKResponse = VKResponseSchema().load(data)
            if vk_response.error:
                self.logger.critical(f"{vk_response.error}")
                return
            data = data["response"]
            self.key = data["key"]
            self.server = data["server"]
            self.ts = data["ts"]
            self.logger.info(f"New VK-API session key has been received")

    async def send_message(self, message: MessageToVK) -> None:
        async with self.session.get(
                self._build_query(
                    host=API_PATH,
                    method="messages.send",
                    params={
                        "user_id": message.user_id,
                        "random_id": random.randint(1, 2 ** 32),
                        "peer_id": "-" + str(self.app.settings.vk.group_id),
                        "message": message.text,
                        "access_token": self.app.settings.vk.token,
                        "keyboard": message.keyboard,
                    },
                ),
        ) as response:
            self.logger.debug(f"Send_message: {await response.json()} {self.ts}")

    async def send_message_event_answer(self, message: EventMessage):
        async with self.session.get(
                self._build_query(
                    host=API_PATH,
                    method="messages.sendMessageEventAnswer",
                    params={
                        "event_id": message.event_id,
                        "user_id": message.user_id,
                        "peer_id": message.peer_id,
                        "event_data": json.dumps(
                            {"text": message.event_data, "type": "show_snackbar"}  # noqa
                        ),
                        "access_token": self.app.settings.vk.token,
                        "keyboard": message.keyboard,
                    },
                ),
        ) as response:
            self.logger.debug(f"Send_message_event: {await response.json()} {self.ts}")

    async def users_get(self, user_id: int):
        async with self.session.get(
                self._build_query(
                    host=API_PATH,
                    method="users.get",
                    params={
                        "user_id": user_id,
                        "access_token": self.app.settings.vk.token,
                    },
                )
        ) as response:
            data: dict[str, list[dict]] = await response.json()
            return (
                    data.get("response")[0].get("first_name", "")
                    + " "
                    + data.get("response")[0].get("last_name", "")
            )

    async def poll(self) -> list[Update]:
        async with self.session.get(
                self._build_query(
                    host=self.server,
                    method="",
                    params={
                        "act": "a_check",
                        "key": self.key,
                        "ts": self.ts,
                        "wait": 30,
                    },
                )
        ) as resp:
            data = await resp.json()
            vk_response: VKResponse = VKResponseSchema().load(data)
            if vk_response.failed == 2:
                self.logger.warning(f"The session key is outdated, we are updating")
                await self._get_long_poll_service()
                return []
            self.ts = vk_response.ts
            self.logger.debug(f"Incoming {resp.status=} {vk_response}")
            return vk_response.updates
