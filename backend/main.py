from fastapi import FastAPI
from routers import users, polls, dev
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

from models.database import engine
from models.user import model as userModel
from models.poll import model as pollModel
from models.poll_options import model as pollOptionsModel
from models.poll_votes import model as pollVotesModel

DEBUG = config('debug', default=False, cast=bool)

userModel.Base.metadata.create_all(bind=engine)
pollModel.Base.metadata.create_all(bind=engine)
pollOptionsModel.Base.metadata.create_all(bind=engine)
pollVotesModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"]
)


app.include_router(users.router)
app.include_router(polls.router)
if DEBUG:
    app.include_router(dev.router)


@app.get('/', tags=["Home"])
def greet():
    return {"message": "Backend aplikacji zespołu Ankieciarze"}
