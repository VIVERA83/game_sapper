import logging
from asyncio import Queue, CancelledError, sleep
from typing import TYPE_CHECKING, Optional, Any
from time import monotonic

from vk_bot.data_classes import MessageFromVK, MessageToVK
from .poller import BasePoller

if TYPE_CHECKING:
    from dispatcher import Bot


class User(BasePoller):
    def __init__(
            self,
            bot: "Bot",
            user_id: int,
            user_name: str,
            timeout: int,
            logger: Optional[logging.Logger] = None,
    ):
        self.bot = bot
        self.user_id = user_id
        self.name = user_name
        # время жизни
        self.timeout = timeout
        # точка отсчета
        self.expired: Optional[float] = None
        # Очередь в которой лежат сообщения от VK
        self.queue_input: Queue[MessageFromVK] = Queue()
        # Текущие меню
        self.current_keyboard: Optional[str] = None
        self.is_running = False
        self.logger = logger or logging.getLogger(self.name)

        # место для хранения каких то данных
        self.data = {}

    async def poller_expired(self):
        """Poller контролирует жизнь User,
        как только пользователь надолго теряет активность, пользователя удаляют из системы
        """
        while self.is_running:
            try:
                await sleep(self.timeout)
            except CancelledError:
                self.is_running = False

            if (self.expired + self.timeout) < monotonic():
                self.is_running = False

        # сообщаем клавиатуре, что мы закончились
        if keyboard := self.bot.get_keyboard_by_name(self.current_keyboard):
            await keyboard.delete_user(self.user_id)
        await self.bot.delete_user(self.user_id)

    async def send_message_to_up(self, message: MessageToVK):
        """Добавление в очередь сообщения на отправку в Bot"""
        self.expired = monotonic()
        message.user_id = self.user_id
        await self.bot.send_message_to_up(message)

    async def send_message_to_down(self, message: MessageFromVK):
        """Отправка сообщение в клавиатуру"""
        #  продлеваем таймаут
        self.expired = monotonic()
        keyboard = self.bot.get_keyboard_by_name(message.payload.keyboard_name)
        await keyboard.send_message_to_down(message)

    async def inbound_message_handler(self):
        """
        Метод обработки входящих сообщений идущих вниз по иерархической ветке,
        необходимо реализовать вечный цикл, с корректным выходом и остановка,
        здесь идет работа с очередью queue_input"""
        while self.is_running:
            try:
                await sleep(self.timeout)
            except CancelledError:
                self.is_running = False
        await self.bot.delete_user(self.user_id)

    def get_setting_keyboard(self, keyboard_name: str) -> Any:
        """Вытаскиваем из User настройки Keyboard, они так же актуальны для игры, если они есть мы их возвращаем,
        иначе применяем настройки по умолчанию"""
        if settings := self.data.get(keyboard_name, None):
            return settings

    def set_setting_keyboard(self, keyboard_name: str, settings: Any = None):
        """Сохраняем настройки клавиатуры"""
        self.data[keyboard_name] = settings
