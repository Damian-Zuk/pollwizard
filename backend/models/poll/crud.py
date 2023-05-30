from sqlalchemy.orm import Session
import html

from . import model, schema
from ..poll_options import crud as optionsCrud


def get_polls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Poll).order_by(model.Poll.created_at.desc()).offset(skip).limit(limit).all()


def get_poll(db: Session, poll_id: int):
    return db.query(model.Poll).filter(model.Poll.id == poll_id).first()


def create_poll(db: Session, poll: schema.PollCreate, userID: int):
    db_poll = model.Poll(title=html.escape(poll.title, quote=True), user_id=userID)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)
    return db_poll


def delete_poll(db: Session, poll: model.Poll):
    optionsCrud.delete_options(db, poll)
    db.delete(poll)
    db.commit()
