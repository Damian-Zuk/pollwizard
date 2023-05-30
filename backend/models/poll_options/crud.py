from sqlalchemy.orm import Session
from typing import List
import html

from . import model

from ..poll.model import Poll
from ..poll_votes import crud as votesCrud


def get_poll_options(db: Session, pollID: int, skip: int = 0, limit: int = 100):
    return db.query(model.PollOptions).filter(model.PollOptions.poll_id==pollID).offset(skip).limit(limit).all()


def get_poll_id(db: Session, optionID: int):
    return db.query(model.PollOptions).filter(model.PollOptions.id==optionID).first().poll_id


def add_options_to_poll(db: Session, options: List[str], pollID: int):
    for option in options:
        db_option = model.PollOptions(value=html.escape(option, quote=True), poll_id=pollID)
        db.add(db_option)
        db.commit()
        db.refresh(db_option)


def delete_options(db: Session, poll: Poll):
    votesCrud.delete_votes(db, poll)
    db.query(model.PollOptions).filter(model.PollOptions.poll_id==poll.id).delete()
