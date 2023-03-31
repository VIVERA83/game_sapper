from sqlalchemy.orm import selectinload

from base.base_accessor import BaseAccessor
from game.data_classes import User
from game.sapper_field import SapperField
from game.models import UserModel
from sqlalchemy import CursorResult, insert, select


class GameAccessor(BaseAccessor):
    async def create_user(self, user: User):
        async with self.app.database.session.begin().session as session:
            async with session:
                query = (
                    insert(UserModel)
                    .values(**user.as_dict)
                    .options(
                        selectinload(UserModel.game_sessions),
                        selectinload(UserModel.rounds),
                    )
                    .returning(UserModel)
                )
                result: CursorResult = await session.execute(query)  # noqa
                await session.commit()
        return result.unique().scalars().first()

    async def get_user_by_vk_id(self, vk_user_id: int):
        async with self.app.database.session.begin().session as session:
            async with session:
                query = select(UserModel).filter(UserModel.id == vk_user_id).options(
                    selectinload(UserModel.game_sessions), selectinload(UserModel.rounds))
                result = await session.execute(query)
                return result.unique().scalars().first()

    async def create_game(self, users: list[int], count_mine: int):
        """Создается игровая сессия"""
        field = SapperField(5, 8, 10).as_str()
        async with self.app.database.session.begin().session as session:
            async with session:
                pass
