from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os


def get_db():

    engine = create_engine(os.environ["DB_URL"])
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_b2b_db():
    engine = create_engine(os.environ["B2B_DB_URL"])
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    print('connection successfull')
    try:
        yield db
    finally:
        db.close()