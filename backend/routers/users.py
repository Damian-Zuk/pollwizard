from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db
from sqlalchemy.orm import Session
from auth.pass_util import verify_password, check_password_complexity
from typing import Annotated
import time

from models.user import schema
from models.user import crud
from models.user import model

from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import signJWT
from auth.jwt_handler import decodeJWT
from auth.jwt_handler import generate_access_token

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
        "session": time.strftime("%H:%M:%S", time.gmtime(int(decodeJWT(token).get("expiry")) - time.time()))
    }


@router.post("/signup")
async def user_signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    errors = {}

    if crud.get_user_by_email(db, user.email):
        errors["email"] = "This email is already in use!"

    if crud.get_user_by_name(db, user.name):
        errors["name"] = "This name is already in use!"

    if check_password_complexity(user.password):
        errors["pass"] = "The password is not complex enough!"

    if len(errors):
        return {"errors": errors}
    
    crud.create_user(db, user)
    return signJWT(user.email)


@router.post("/login")
def user_login(user: schema.UserLogin, db: Session = Depends(get_db)):
    tryLogin = crud.get_user_by_email(db, user.email)
    if tryLogin:
        if verify_password(user.password, tryLogin.password):
            return signJWT(user.email)
    raise HTTPException(status_code=403, detail="Invalid email address or password!")


@router.post("/refresh")
def user_login(refresh_token: Annotated[str, Depends(JWTBearer(token_type="refresh"))]):
    try:
        user_email = decodeJWT(refresh_token).get("user_email")
        return generate_access_token(user_email)
    except:
        raise HTTPException(status_code=500, detail="JWT decode error.")


def get_user_identity(token: Annotated[str, Depends(JWTBearer())], db: Session = Depends(get_db)):
    try:
        userEmail = decodeJWT(token).get("user_email")
        return crud.get_user_by_email(db, userEmail)
    except:
        return model.User(id=0)
