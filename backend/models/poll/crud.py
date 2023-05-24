from sqlalchemy.orm import Session

from . import model, schema


def get_polls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Poll).offset(skip).limit(limit).all()


def get_poll(db: Session, poll_id: int):
    return db.query(model.Poll).filter(model.Poll.id == poll_id).first()


def create_poll(db: Session, poll: schema.PollCreate, userID: int):
    db_poll = model.Poll(title=poll.title, user_id=userID)
    db.add(db_poll)
    db.commit()
    db.refresh(db_poll)
    return db_poll
