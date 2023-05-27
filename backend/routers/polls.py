from fastapi import APIRouter, Depends, Header
from auth.jwt_bearer import JWTBearer
from dependencies import get_db
from sqlalchemy.orm import Session
from typing import Annotated

from models.user.model import User
from models.user import crud as userCrud
from .users import get_user_identity

from models.poll.model import Poll
from models.poll import crud as pollCrud
from models.poll import schema

from models.poll_options.model import PollOptions
from models.poll_options import crud as optionCrud
from models.poll_votes import crud as voteCrud


router = APIRouter(
    prefix="/polls",
    tags=["Polls"],
    responses={404: {"description": "Not found"}},
)


def create_get_response(polls : list[Poll], db: Session, auth_user: User=None):
    return [{
        "id": poll.id,
        "title": poll.title,
        "created_at": poll.created_at,
        "created_by": userCrud.get_user(db, poll.user_id).name,
        "voted_for": voteCrud.get_user_vote_id(db, auth_user, poll) if auth_user else -1,
        "options": [{
            "id": option.id,
            "value": option.value,
            "votes": len(option.votes)
        } for option in poll.options ]
    } for poll in polls ]


@router.get("/")
async def get_polls(poll_id: int, db: Session = Depends(get_db), authorization: str = Header(default=None)):
    poll = pollCrud.get_poll(db, poll_id)
    if authorization:
        token = authorization.split(" ")[1]
        user = get_user_identity(token, db)
        return create_get_response([poll], db, user)
    return create_get_response([poll], db)


@router.get("/all")
async def get_polls(db: Session = Depends(get_db), authorization: str = Header(default=None)):
    polls = pollCrud.get_polls(db)
    if authorization:
        token = authorization.split(" ")[1]
        user = get_user_identity(token, db)
        return create_get_response(polls, db, user)
    return create_get_response(polls, db)


@router.get("/my-polls")
async def get_user_polls(token: Annotated[str, Depends(JWTBearer())], db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    return create_get_response(user.polls, db)


@router.post("/")
async def create_poll(token: Annotated[str, Depends(JWTBearer())], poll: schema.PollCreate, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    
    if not len(poll.title):
        return {"error": "Poll title cannot be empty!"}
    if len(poll.options) < 2:
        return {"error": "Poll must containt at least 2 options!"}
    for option in poll.options:
        if not len(option):
            return {"error": "Poll option cannot be empty!"}
    
    created_poll = pollCrud.create_poll(db, poll, user.id)
    optionCrud.add_options_to_poll(db, poll.options, created_poll.id)
    return {"id": created_poll.id}
    

@router.post("/vote")
async def vote_for_poll(token: Annotated[str, Depends(JWTBearer())], optionID: int, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    
    if not db.query(PollOptions).filter(PollOptions.id==optionID).count():
        return {"error": "Option doesn't exists."}

    poll = pollCrud.get_poll(db, optionCrud.get_poll_id(db, optionID))
    if voteCrud.get_user_vote_id(db, user, poll) != -1:
        return {"error": "You already voted for this poll!"}
    
    return voteCrud.vote_for_poll(db, user.id, optionID)
