from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from ..database import Base


class PollVotes(Base):
    __tablename__ = "poll_votes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    poll_option_id: Mapped[int] = mapped_column(ForeignKey("poll_options.id"))

    def __repr__(self) -> str:
        return f"Poll(id={self.id!r}, title={self.user_id!r})"
