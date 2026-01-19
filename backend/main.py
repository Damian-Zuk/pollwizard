from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers import users, polls, dev
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
import logging

from fastapi_limiter import FastAPILimiter

from security.fastapi_jwt_redis import JwtManager

from models.database import engine
from models.user import model as userModel
from models.poll import model as pollModel
from models.poll_options import model as pollOptionsModel
from models.poll_votes import model as pollVotesModel

from config import *

userModel.Base.metadata.create_all(bind=engine)
pollModel.Base.metadata.create_all(bind=engine)
pollOptionsModel.Base.metadata.create_all(bind=engine)
pollVotesModel.Base.metadata.create_all(bind=engine)

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s][%(asctime)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handlers=[logging.StreamHandler(), logging.FileHandler("server.log")],
)

JwtManager.configure(
    secret=JWT_SECRET,
    redis_host=REDIS_HOST,
    redis_port=REDIS_PORT,
    redis_pass=REDIS_PASS,
    redis_db_index=JWT_REDIS_INDEX
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = f"redis://:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}/{RATE_LIMITER_REDIS_INDEX}"
    redis_instance = redis.from_url(
        redis_url,
        encoding="utf-8",
        decode_responses=True,
    )
    await FastAPILimiter.init(redis_instance)
    yield 
    await redis_instance.close()

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)
app.include_router(polls.router)
if DEBUG:
    app.include_router(dev.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/', tags=["Home"])
def greet():
    return {"message": "Backend aplikacji zespołu Ankieciarze"}

