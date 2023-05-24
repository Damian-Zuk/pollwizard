from fastapi import APIRouter, Depends
from auth.jwt_bearer import JWTBearer
from dependencies import get_db
from sqlalchemy.orm import Session
from models.poll import schema
from models.poll_options import schema as optionSchema
from models.poll import crud
from models.user import crud as userCrud
from models.poll_options import crud as optionCrud
from models.poll_votes import crud as voteCrud
from typing import Annotated, List
from .users import get_user_identity

router = APIRouter(
    prefix="/polls",
    tags=["Polls"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_polls(db: Session = Depends(get_db)):
    result =[]
    polls = crud.get_polls(db)
    for poll in polls:
        tmp = {}
        tmp["id"] = poll.id
        tmp["title"] = poll.title
        tmp["created_by"] = userCrud.get_user(db, poll.user_id).name
        tmp["created_at"] = poll.created_at
        options = []
        for option in poll.options:
            options.append({
                "id": option.id,
                "value": option.value,
                "votes": len(option.votes)
            })
        tmp["options"] = options
        result.append(tmp)
    return result


@router.get("/my-polls")
async def get_user_polls(token: Annotated[str, Depends(JWTBearer())], db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    result =[]
    polls = user.polls
    for poll in polls:
        tmp = {}
        tmp["id"] = poll.id
        tmp["title"] = poll.title
        tmp["created_by"] = user.name
        tmp["created_at"] = poll.created_at
        options = []
        for option in poll.options:
            options.append({
                "id": option.id,
                "value": option.value,
                "votes": len(option.votes)
            })
        tmp["options"] = options
        result.append(tmp)
    return result


@router.post("/")
async def create_poll(token: Annotated[str, Depends(JWTBearer())], poll: schema.PollCreate, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    return crud.create_poll(db, poll, user.id)


@router.post("/add-options")
async def create_poll(token: Annotated[str, Depends(JWTBearer())], pollID: int,  options: List[optionSchema.OptionCreate], db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    pollToAdd = None
    for poll in user.polls:
        if poll.id == pollID:
            pollToAdd = poll
    return optionCrud.add_options_to_poll(db, options, pollToAdd.id)


@router.post("/vote")
async def vote_for_poll(token: Annotated[str, Depends(JWTBearer())], optionID: int, db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    return voteCrud.vote_for_poll(db, user.id, optionID)
