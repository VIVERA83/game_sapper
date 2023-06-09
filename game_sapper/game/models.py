from game.data_classes import User, Round, GameSession
from store.database.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserGameSessionModel(Base):
    __tablename__ = "user_game_session"  # noqa

    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=True)
    game_session_id: Mapped[int] = Column(Integer, ForeignKey("game_sessions.id"), primary_key=True, nullable=True)


class UserModel(Base):
    __tablename__ = "users"  # noqa

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vk_user_id: Mapped[int] = Column(Integer, unique=True)
    username: Mapped[str] = Column(String, default="")
    game_sessions: Mapped[list["GameSessionModel"]] = relationship(
        secondary=UserGameSessionModel.__table__, back_populates="users", lazy="joined")
    rounds: Mapped[list["RoundModel"]] = relationship(lazy="joined")

    @property
    def as_dataclass(self) -> "User":
        return User(
            id=self.id,
            vk_user_id=self.vk_user_id,
            username=self.username,
            game_sessions=[game_session.as_dataclass for game_session in self.game_sessions],
            rounds=[round_.as_dataclass for round_ in self.rounds],
        )


class GameSessionModel(Base):
    __tablename__ = "game_sessions"  # noqa

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    field: Mapped[str] = Column(String, nullable=False)
    users: Mapped[list["UserModel"]] = relationship(
        secondary=UserGameSessionModel.__table__,
        back_populates="game_sessions",
        lazy="joined",
    )
    rounds: Mapped[list["RoundModel"]] = relationship(lazy="joined")

    @property
    def as_dataclass(self) -> "GameSession":
        return GameSession(
            id=self.id,
            field=self.field,
            rounds=[round_.as_dataclass for round_ in self.rounds],
            users=[
                User(
                    id=user.id,
                    vk_user_id=user.vk_user_id,
                    username=user.username,
                    game_sessions=[],
                    rounds=[],
                )
                for user in self.users
            ],
        )


class RoundModel(Base):
    __tablename__ = "rounds"  # noqa

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    game_session_id: Mapped[int] = mapped_column(ForeignKey("game_sessions.id"))
    round_number: Mapped[int] = Column(Integer, nullable=False, )
    player_id: Mapped[int] = Column(Integer, nullable=False)
    cords: Mapped[str] = Column(String, nullable=False)
    result: Mapped[str] = Column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))


    @property
    def as_dataclass(self) -> "Round":
        return Round(
            id=self.id,
            game_session_id=self.game_session_id,
            round_number=self.round_number,
            player_id=self.player_id,
            cords=self.cords,
            result=self.result
        )
