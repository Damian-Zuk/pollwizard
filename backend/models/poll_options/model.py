from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy import String
from ..database import Base
from ..poll_votes import model as pollVotesModel


class PollOptions(Base):
    __tablename__ = "poll_options"
    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(100))
    poll_id: Mapped[int] = mapped_column(ForeignKey("poll.id"))
    votes: Mapped[List["pollVotesModel.PollVotes"]] = relationship()

    def __repr__(self) -> str:
        return f"Poll(id={self.id!r}, title={self.value!r})"
