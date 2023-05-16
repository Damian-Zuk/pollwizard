from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

config = {}
with open("config.ini", "r") as f:
    for entry in f.read().split("\n"):
        if len(entry):
            e = entry.split("=")
            config[e[0].strip()] = e[1].strip() 

DATABASE_URL = f"mysql+pymysql://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_HOST']}:3306/{config['DB_NAME']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
