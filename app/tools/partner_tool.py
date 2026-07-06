from sqlalchemy import text
from database.connection import get_b2b_db
from dotenv import load_dotenv
from langchain.tools import tool
from typing import Optional

load_dotenv()

@tool
def partner_index(limit: int = 10, offset: int = 0) -> dict:

    """
        This toll will pick the partners list from the partner table
         Args:
            limit: Maximum number of records to return (default 10, max 50).
            offset: Number of records to skip for pagination (default 0).
        Returns:
            Dict with 'data' (list of loan requests), 'total' count, and pagination info.
    """

    db = next(get_b2b_db())
    limit = min(limit,10)
    try:
        total: int = db.execute(text("SELECT count(*) FROM partner")).scalar() or 0
        result = db.execute(text("""
            SELECT * FROM partner LIMIT :limit OFFSET :offset
        """),
        {
            "limit": limit,
            "offset": offset
        }).fetchall()

        return {
                "data": [dict(row._mapping) for row in result],
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": (offset + limit) < total
            }
    finally:
        db.close()
