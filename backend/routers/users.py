from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db
from sqlalchemy.orm import Session
from auth.pass_util import verify_password, check_password_complexity
from typing import Annotated
import time
import re

from models.user import schema
from models.user import crud
from models.user import model

from auth.jwt_bearer import JWTBearer
from auth.jwt_bearer import signJWT
from auth.jwt_bearer import decodeJWT
from auth.jwt_bearer import generate_access_token


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_user_data(token: Annotated[str, Depends(JWTBearer())], db: Session = Depends(get_db)):
    user = get_user_identity(token, db)
    return {
        "name": user.name,
        "email": user.email,
        "session": time.strftime("%H:%M:%S", time.gmtime(int(decodeJWT(token).get("exp")) - time.time()))
    }


@router.post("/signup")
async def user_signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    errors = {}

    if crud.get_user_by_email(db, user.email):
        errors["email"] = "This email address is already in use. Please choose another one."

    if crud.get_user_by_name(db, user.name):
        errors["name"] = "This username is already taken. Please pick a different one."

    if not check_password_complexity(user.password):
        errors["pass"] = "The password does not meet the complexity requirements."

    if re.match(r"^[a-zA-Z0-9_]+$", user.name) is None:
        errors["name"] = "Invalid username. Please use only letters, numbers, and underscores."

    if len(errors):
        raise HTTPException(status_code=422, detail={"errors": errors})
    
    crud.create_user(db, user)
    return signJWT(user.email)


@router.post("/login")
def user_login(user: schema.UserLogin, db: Session = Depends(get_db)):
    user_db = crud.get_user_by_email(db, user.email)
    if user_db and verify_password(user.password, user_db.password):
            return signJWT(user_db.email)
    raise HTTPException(status_code=403, detail="Invalid email address or password!")


@router.post("/refresh")
def user_login(refresh_token: Annotated[str, Depends(JWTBearer(token_type="refresh"))]):
    user_email = decodeJWT(refresh_token).get("user_email")
    return generate_access_token(user_email)


def get_user_identity(token: str, db: Session):
    try:
        user_email = decodeJWT(token).get("user_email")
        return crud.get_user_by_email(db, user_email)
    except AttributeError:
        return model.User(id=0)
