from fastapi import APIRouter, Depends
from dependencies import get_db
from sqlalchemy.orm import Session
from models.user import schema
from models.user import crud
from auth.jwt_handler import signJWT
from auth.pass_util import verify_password

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@router.get("/{userID}")
async def get_user(userID: str, db: Session = Depends(get_db)):
    return crud.get_user(db, userID)


@router.post("/")
async def add_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    crud.create_user(db, user)
    return {"message": "Dodano usera!"}


@router.delete("/{userID}")
async def del_user(userID: str, db: Session = Depends(get_db)):
    return crud.delete_user(db, userID)


@router.post("/signup")
async def user_signup(user: schema.UserCreate, db: Session = Depends(get_db)):
    errors = { "errors": {} }

    if crud.get_user_by_email(db, user.email):
        errors["errors"]["email"] = "This email is already in use!"
    
    if crud.get_user_by_name(db, user.name):
        errors["errors"]["name"] = "This name is already in use!"
    
    if len(errors["errors"]):
        return errors
    
    crud.create_user(db, user)
    return signJWT(user.email, user.name)


@router.post("/login")
def user_login(user: schema.UserLogin, db: Session = Depends(get_db)):
    tryLogin = crud.get_user_by_email(db, user.email)
    if tryLogin:
        if verify_password(user.password, tryLogin.password):
            return signJWT(user.email, tryLogin.name)
    return {
        "error": "Invalid login details!"
    }
