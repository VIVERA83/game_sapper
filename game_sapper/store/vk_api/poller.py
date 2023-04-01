import asyncio
from asyncio import Task, CancelledError
from typing import Optional

from store import Store


class Poller:
    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_from_vk_task: Optional[Task] = None

    async def start(self):
        self.is_running = True
        self.poll_from_vk_task = asyncio.create_task(self.poll())

    async def stop(self):
        self.is_running = False
        self.poll_from_vk_task.cancel()
        await self.poll_from_vk_task
        self.store.bots_manager.logger.info("Stopped VK_API polling")

    async def poll(self):
        while self.is_running:
            try:
                updates = await self.store.vk_api.poll()
                await self.store.bots_manager.handle_updates(updates)
            except CancelledError:
                self.is_running = False
