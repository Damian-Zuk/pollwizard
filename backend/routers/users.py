
from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

import time
import re
import logging
from typing import Annotated

from dependencies import get_db
from security.fastapi_jwt_redis import JwtManager, JwtBearer, TokenType, AuthCredentials
from security.pass_util import verify_password, check_password_complexity

from models.user import schema
from models.user import crud
from models.user.model import User 


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(RateLimiter(times=10, seconds=10))],
)


@router.get("/")
async def get_user_data(
    credentials: Annotated[AuthCredentials, Depends(JwtBearer())],
    db: Session = Depends(get_db)
):
    user = get_user_identity(credentials, db)
    session_time = time.gmtime(int(credentials.exp) - time.time())
    return {
        "name": user.name,
        "email": user.email,
        "session": time.strftime("%H:%M:%S", session_time)
    }


@router.post("/signup", dependencies=[Depends(RateLimiter(times=3, seconds=60))])
async def user_signup(
    user: schema.UserCreate,
    db: Session = Depends(get_db)
):
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
    
    user_db = crud.create_user(db, user)
    return JwtManager.generate_token_pair({"user_id": user_db.id})


@router.post("/login")
async def user_login(
    user: schema.UserLogin, 
    db: Session = Depends(get_db)
):
    user_db = crud.get_user_by_email(db, user.email)
    if user_db and verify_password(user.password, user_db.password):
        return JwtManager.generate_token_pair({"user_id": user_db.id})
    raise HTTPException(status_code=401, detail="Invalid email address or password.")


@router.post("/refresh")
async def refresh(credentials: Annotated[AuthCredentials, Depends(JwtBearer(TokenType.REFRESH))]):
    return JwtManager.refresh_token_pair(credentials)


@router.post("/logout", status_code=204)
async def logout(credentials: Annotated[AuthCredentials, Depends(JwtBearer())]):
    JwtManager.revoke_token(credentials)


def get_user_identity(credentials: AuthCredentials, db: Session) -> User:
    user = crud.get_user(db, credentials["user_id"])
    if user is None:
        logging.error("<users::get_user_identity> User not found.")
        raise HTTPException(status_code=401, detail="Invalid bearer token.")
    return user
