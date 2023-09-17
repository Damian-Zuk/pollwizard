from fastapi import APIRouter, Depends, HTTPException
from auth.jwt_bearer import JWTBearer
from dependencies import get_db
from sqlalchemy.orm import Session
from typing import Annotated

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


def compose_polls_response(polls : list[Poll], db: Session):
    return [{
        "id": poll.id,
        "title": poll.title,
        "created_at": poll.created_at,
        "created_by": userCrud.get_user(db, poll.user_id).name,
        "options": [{
            "id": option.id,
            "value": option.value,
            "votes": len(option.votes)
        } for option in poll.options ]
    } for poll in polls ]


@router.get("/")
async def get_poll(poll_id: int, db: Session = Depends(get_db)):
    poll = pollCrud.get_poll(db, poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found.")
    return compose_polls_response([poll], db)


@router.get("/all")
async def get_polls(db: Session = Depends(get_db)):
    polls = pollCrud.get_polls(db)
    return compose_polls_response(polls, db)


@router.get("/user")
async def get_user_polls(username: str, db: Session = Depends(get_db)):
    user = userCrud.get_user_by_name(db, username)
    return compose_polls_response(user.polls, db)


@router.post("/", status_code=201)
async def create_poll(token: Annotated[str, Depends(JWTBearer())], poll: schema.PollCreate, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    created_poll = pollCrud.create_poll(db, poll, user.id)
    optionCrud.add_options_to_poll(db, poll.options, created_poll.id)
    return {"id": created_poll.id} 
 

@router.post("/vote", status_code=201)
async def vote_for_poll(token: Annotated[str, Depends(JWTBearer())], option_id: int, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)

    if not db.query(PollOptions).filter(PollOptions.id==option_id).count():
        raise HTTPException(status_code=422, detail="The selected poll option does not exist.")

    poll = pollCrud.get_poll(db, optionCrud.get_poll_id(db, option_id))
    if voteCrud.get_user_vote(db, user.id, poll.id) != -1:
        raise HTTPException(status_code=422, detail="You have already voted on this poll.")
    
    return voteCrud.vote_for_poll(db, user.id, option_id)


@router.get("/my-votes")
async def get_user_vote(token: Annotated[str, Depends(JWTBearer())], poll_ids: str, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    return { poll_id: voteCrud.get_user_vote(db, user.id, poll_id) for poll_id in poll_ids.split(',') }


@router.delete("/")
async def delete_poll(token: Annotated[str, Depends(JWTBearer())], poll_id: int, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    poll = pollCrud.get_poll(db, poll_id)
    
    if user.id != poll.user_id:
        raise HTTPException(status_code=403, detail="You are not the author of this poll.")
    
    pollCrud.delete_poll(db, poll)
    return {"detail": "The poll has been deleted."}
