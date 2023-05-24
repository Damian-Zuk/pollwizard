from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from models.user import schema
from models.user import crud
from models.user import model
from auth.jwt_handler import signJWT
from auth.pass_util import verify_password, check_password_complexity
from typing import Annotated
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import decodeJWT
import time

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
    errors = {"errors": {}}

    if crud.get_user_by_email(db, user.email):
        errors["errors"]["email"] = "This email is already in use!"

    if crud.get_user_by_name(db, user.name):
        errors["errors"]["name"] = "This name is already in use!"

    if check_password_complexity(user.password):
        errors["errors"]["pass"] = "The password is not complex enough!"

    if user.password != user.repassword:
        errors["errors"]["repass"] = "The passwords are not the same!"

    if len(errors["errors"]):
        return errors

    crud.create_user(db, user)
    return signJWT(user.email)


@router.post("/login")
def user_login(user: schema.UserLogin, db: Session = Depends(get_db)):
    tryLogin = crud.get_user_by_email(db, user.email)
    if tryLogin:
        if verify_password(user.password, tryLogin.password):
            return signJWT(user.email)
    return {
        "error": "Invalid login details!"
    }


def get_user_identity(token: Annotated[str, Depends(JWTBearer())], db: Session = Depends(get_db)):
    try:
        userEmail = decodeJWT(token).get("userID")
        return crud.get_user_by_email(db, userEmail)
    except:
        return model.User(id=0)
