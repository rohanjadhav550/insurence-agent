from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.environ["DB_URL"])
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()