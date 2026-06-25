from sqlalchemy import text
from database.connection import get_b2b_db
from dotenv import load_dotenv
load_dotenv()

def index():
    db = next(get_b2b_db())
    result = db.execute(text("SELECT * FROM loan_request")).fetchall()
    print(result)

index()