from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

DATABASE_URL = f"postgresql://{config('db_user')}:{config('db_pass')}@{config('db_host')}:{config('db_port')}/{config('db_name')}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
