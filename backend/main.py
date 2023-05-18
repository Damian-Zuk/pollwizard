from fastapi import FastAPI
from routers import users, polls
from fastapi.middleware.cors import CORSMiddleware

from models.database import engine
from models.user import model as userModel

from fastapi.responses import JSONResponse
import json

userModel.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "PUT", "DELETE"]
)


app.include_router(users.router)
app.include_router(polls.router)


@app.get("/polls")
def polls():
    # temporary
    with open("testing/get-polls.json", "r") as f:
        content = json.load(f)
    return JSONResponse(content=content)