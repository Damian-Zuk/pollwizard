from sqlalchemy.orm import Session

from . import model
from ..user.model import User
from ..poll.model import Poll
from ..poll_options import crud


def vote_for_poll(db: Session, userID: int, optionID: int):
    db_vote = model.PollVotes(poll_option_id=optionID, user_id=userID)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


def get_user_vote(db: Session, user: User, poll: Poll):
    poll_options = crud.get_poll_options(db, poll.id)
    user_vote = (
        db.query(model.PollVotes)
        .filter(model.PollVotes.user_id == user.id)
        .filter(model.PollVotes.poll_option_id.in_([option.id for option in poll_options]))
        .first()
    )
    if user_vote is None:
        return -1
    return user_vote.poll_option_id
