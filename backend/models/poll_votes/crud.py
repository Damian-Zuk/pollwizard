from sqlalchemy.orm import Session

from . import model

def vote_for_poll(db: Session, userID: int, optionID: int):
    db_vote = model.PollVotes(poll_option_id=optionID, user_id=userID)
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote
