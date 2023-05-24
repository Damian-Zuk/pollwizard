from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from models.user import crud

router = APIRouter(
    prefix="/dev",
    tags=["Dev"],
    responses={404: {"description": "Not found"}},
)


@router.get("/users")
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.get("/users/{userID}")
async def get_user(userID: str, db: Session = Depends(get_db)):
    return crud.get_user(db, userID)


@router.delete("/users/{userID}")
async def del_user(userID: str, db: Session = Depends(get_db)):
    return crud.delete_user(db, userID)
