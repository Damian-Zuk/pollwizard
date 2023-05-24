from sqlalchemy.orm import Session
from typing import List

from . import model, schema


def get_poll_options(db: Session, pollID: int, skip: int = 0, limit: int = 100):
    return db.query(model.PollOptions).filter(poll_id=pollID).offset(skip).limit(limit).all()


def add_options_to_poll(db: Session, options: List[schema.OptionCreate], pollID: int):
    created = {}
    for option in options:
        db_option = model.PollOptions(value=option.value, poll_id=pollID)
        db.add(db_option)
        db.commit()
        db.refresh(db_option)
    return created
