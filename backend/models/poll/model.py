from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from typing import List
from sqlalchemy import String
from ..database import Base
from ..poll_options import model as pollOptionsModel


class Poll(Base):
    __tablename__ = "poll"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    options: Mapped[List["pollOptionsModel.PollOptions"]] = relationship()

    def __repr__(self) -> str:
        return f"Poll(id={self.id!r}, title={self.title!r})"
