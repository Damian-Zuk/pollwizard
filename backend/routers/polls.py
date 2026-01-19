from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
from typing import Annotated, List

from dependencies import get_db
from security.fastapi_jwt_redis import JwtBearer, AuthCredentials

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
    dependencies=[Depends(RateLimiter(times=10, seconds=10))]
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
async def get_poll(
    poll_id: int,
    db: Session = Depends(get_db)
):
    poll = pollCrud.get_poll(db, poll_id)
    if poll is None:
        raise HTTPException(status_code=404, detail="Poll not found.")
    return compose_polls_response([poll], db)


@router.get("/all")
async def get_polls(
    db: Session = Depends(get_db)
):
    polls = pollCrud.get_polls(db)
    return compose_polls_response(polls, db)


@router.get("/user")
async def get_user_polls(
    username: str,
    db: Session = Depends(get_db)
):
    user = userCrud.get_user_by_name(db, username)
    return compose_polls_response(user.polls, db)


@router.post("/", status_code=201, dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def create_poll(
    credentials: Annotated[AuthCredentials, Depends(JwtBearer())],
    poll: schema.PollCreate,
    db: Session = Depends(get_db)
):   
    user = get_user_identity(credentials, db)
    created_poll = pollCrud.create_poll(db, poll, user.id)
    optionCrud.add_options_to_poll(db, poll.options, created_poll.id)
    return {"id": created_poll.id} 
 

@router.post("/vote", status_code=201)
async def vote_for_poll(
    credentials: Annotated[AuthCredentials, Depends(JwtBearer())],
    option_id: int,
    db: Session = Depends(get_db)
):
    user = get_user_identity(credentials, db)
    if not db.query(PollOptions).filter(PollOptions.id==option_id).count():
        raise HTTPException(status_code=422, detail="The selected poll option does not exist.")

    poll = pollCrud.get_poll(db, optionCrud.get_poll_id(db, option_id))
    if voteCrud.get_user_vote(db, user.id, poll.id) != -1:
        raise HTTPException(status_code=422, detail="You have already voted on this poll.")
    
    return voteCrud.vote_for_poll(db, user.id, option_id)


@router.get("/my-votes")
async def get_user_vote(
    credentials: Annotated[AuthCredentials, Depends(JwtBearer())],
    poll_ids: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
):
    user = get_user_identity(credentials, db)

    ids = [int(pid) for pid in poll_ids.split(",") if pid.strip().isdigit()]
    if not ids:
        raise HTTPException(400, "poll_ids must contain at least one valid ID")

    return {
        poll_id: voteCrud.get_user_vote(db, user.id, poll_id)
        for poll_id in ids
    }


@router.delete("/")
async def delete_poll(
    credentials: Annotated[AuthCredentials, Depends(JwtBearer())],
    poll_id: int,
    db: Session = Depends(get_db)
):
    user = get_user_identity(credentials, db)
    poll = pollCrud.get_poll(db, poll_id)
    
    if user.id != poll.user_id:
        raise HTTPException(status_code=403, detail="You are not the author of this poll.")
    
    pollCrud.delete_poll(db, poll)
    return {"detail": "The poll has been deleted."}
