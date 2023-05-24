from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from typing import List
from ..database import Base
from ..poll import model as pollModel
from ..poll_votes import model as pollVotesModel


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    polls: Mapped[List["pollModel.Poll"]] = relationship()
    votes: Mapped[List["pollVotesModel.PollVotes"]] = relationship()

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
