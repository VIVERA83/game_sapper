import asyncio
from asyncio import Task, CancelledError
from typing import Optional

from store import Store
from vk_bot.data_classes import TypeMessage


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        self.is_running = True
        self.poll_task = asyncio.create_task(self.poll())

    async def stop(self):
        self.is_running = False
        self.poll_task.cancel()
        await self.poll_task
        self.store.bots_manager.logger.info("Stopped Bot manager polling")

    async def poll(self):
        while self.is_running:
            try:
                message = await self.store.bots_manager.vk_bot.queue_output.get()
                self.store.bots_manager.vk_bot.queue_output.task_done()
                if message.type.value == TypeMessage.message_event.value:
                    await self.store.vk_api.send_message_event_answer(message)
                else:
                    await self.store.vk_api.send_message(message)
            except CancelledError:
                self.is_running = False
