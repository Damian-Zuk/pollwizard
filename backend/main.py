from fastapi import FastAPI
from routers import users, polls

from models.database import engine
from models.user import model as userModel

userModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(polls.router)


@app.get('/', tags=["Home"])
def greet():
    return {"message": "Backend aplikacji zespołu Ankieciarze"}
