from sqlalchemy.orm import Session

from . import model
from ..poll_options import crud

from ..user.model import User
from ..poll.model import Poll


def vote_for_poll(db: Session, userID: int, optionID: int):
    db_vote = model.PollVotes(poll_option_id=optionID, user_id=userID)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote


def get_user_vote(db: Session, userID: User, pollID: Poll):
    poll_options = crud.get_poll_options(db, pollID)
    user_vote = (
        db.query(model.PollVotes)
        .filter(model.PollVotes.user_id == userID)
        .filter(model.PollVotes.poll_option_id.in_([option.id for option in poll_options]))
        .first()
    )
    return user_vote.poll_option_id if user_vote is not None else -1


def delete_votes(db: Session, poll: Poll):
    poll_options = crud.get_poll_options(db, poll.id)
    db.query(model.PollVotes).filter(model.PollVotes.poll_option_id.in_([option.id for option in poll_options])).delete()
