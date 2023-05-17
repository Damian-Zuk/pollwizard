from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

# config = {}
# with open("config.ini", "r") as f:
#     for entry in f.read().split("\n"):
#         if len(entry):
#             e = entry.split("=")
#             config[e[0].strip()] = e[1].strip()

DATABASE_URL = f"mysql+pymysql://{config('db_user')}:{config('db_pass')}@{config('db_host')}:{config('db_port')}/{config('db_name')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
