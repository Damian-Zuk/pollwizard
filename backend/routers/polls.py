from fastapi import APIRouter, Depends
from auth.jwt_bearer import JWTBearer
from dependencies import get_db
from sqlalchemy.orm import Session
from models.user import crud as userCrud
from models.user.model import User
from models.poll import schema
from models.poll import crud
from models.poll_options import crud as optionCrud
from models.poll_votes import crud as voteCrud
from models.poll import crud as pollCrud
from models.poll.model import Poll
from models.poll_options.model import PollOptions
from typing import Annotated, List
from .users import get_user_identity

router = APIRouter(
    prefix="/polls",
    tags=["Polls"],
    responses={404: {"description": "Not found"}},
)


def create_get_response(polls : list[Poll], db: Session, auth_user: User=None):
    return [{
        "id": poll.id,
        "title": poll.title,
        "created_by": userCrud.get_user(db, poll.user_id).name,
        "created_at": poll.created_at,
        "voted_for": voteCrud.get_user_vote(db, auth_user, poll) if auth_user else -1,
        "options": [
            {
                "id": option.id,
                "value": option.value,
                "votes": len(option.votes)
            } for option in poll.options ]
        } for poll in polls ]


@router.get("/one")
async def get_polls(poll_id: int, db: Session = Depends(get_db)):
    poll = crud.get_poll(db, poll_id)
    return create_get_response([poll], db)

@router.get("/one-auth")
async def get_polls(token: Annotated[str, Depends(JWTBearer())], poll_id: int, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    poll = crud.get_poll(db, poll_id)
    return create_get_response([poll], db, user)


@router.get("/all")
async def get_polls(db: Session = Depends(get_db)):
    polls = crud.get_polls(db)
    return create_get_response(polls, db)


@router.get("/all-auth")
async def get_polls(token: Annotated[str, Depends(JWTBearer())], db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    polls = crud.get_polls(db)
    return create_get_response(polls, db, user)


@router.get("/my-polls")
async def get_user_polls(token: Annotated[str, Depends(JWTBearer())], db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    return create_get_response(user.polls, db)


@router.post("/")
async def create_poll(token: Annotated[str, Depends(JWTBearer())], poll: schema.PollCreate, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    if not len(poll.title):
        return {"error": "Poll title cannot be empty!"}
    if len(poll.options) > 1:
        for option in poll.options:
            if not len(option):
                return {"error": "Poll option cannot be empty!"}
        created_poll = crud.create_poll(db, poll, user.id)
        optionCrud.add_options_to_poll(db, poll.options, created_poll.id)
        return {"id": created_poll.id}
    return {"error": "Poll must containt at least 2 options!"}


@router.post("/vote")
async def vote_for_poll(token: Annotated[str, Depends(JWTBearer())], optionID: int, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    
    if not db.query(PollOptions).filter(PollOptions.id==optionID).count():
        return {"error": "Option doesn't exists."}

    poll = pollCrud.get_poll(db, optionCrud.get_poll_id(db, optionID))
    if voteCrud.get_user_vote(db, user, poll) != -1:
        return {"error": "You already voted for this poll!"}
    
    return voteCrud.vote_for_poll(db, user.id, optionID)
