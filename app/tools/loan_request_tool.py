from sqlalchemy import text
from database.connection import get_b2b_db
from dotenv import load_dotenv
from langchain.tools import tool
from typing import Optional

load_dotenv()


@tool
def index(limit: int = 10, offset: int = 0) -> dict:
    """
    Fetch all loan requests from the loan_request table with pagination.
    Use this tool when you want to retrieve all loan requests from the system.

    Args:
        limit: Maximum number of records to return (default 10, max 50).
        offset: Number of records to skip for pagination (default 0).

    Returns:
        Dict with 'data' (list of loan requests), 'total' count, and pagination info.
    """
    limit = min(limit, 50)

    db = next(get_b2b_db())
    try:
        total: int = db.execute(text("SELECT COUNT(*) FROM loan_request")).scalar() or 0

        result = db.execute(
            text("SELECT * FROM loan_request LIMIT :limit OFFSET :offset"),
            {"limit": limit, "offset": offset}
        ).fetchall()

        return {
            "data": [dict(row._mapping) for row in result],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }
    finally:
        db.close()


@tool
def show(case_id: str) -> dict:
    """
    Fetch a single loan request by case ID.
    Use this tool when you want to retrieve a specific loan request using its case ID.

    Args:
        case_id: The numeric case ID of the loan request (passed as a string).

    Returns:
        A single loan request record as a dict, or empty dict if not found.
    """
    db = next(get_b2b_db())
    try:
        result = db.execute(
            text("SELECT * FROM loan_request WHERE case_id = :case_id"),
            {"case_id": case_id}
        ).fetchone()

        return dict(result._mapping) if result else {}
    finally:
        db.close()


@tool
def show_by_name(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> dict:
    """
    Fetch loan requests by first name, last name, or both using partial matching.
    Use this tool when you want to search loan requests by applicant name.

    Args:
        first_name: The first name (or partial first name) of the loan request holder.
        last_name: The last name (or partial last name) of the loan request holder.
        limit: Maximum number of records to return (default 10, max 50).
        offset: Number of records to skip for pagination (default 0).

    Returns:
        Dict with 'data' (list of matching loan requests) and pagination info.
    """
    limit = min(limit, 50)

    db = next(get_b2b_db())
    try:
        params = {
            "first_name": f"%{first_name}%" if first_name else "%",
            "last_name": f"%{last_name}%" if last_name else "%",
        }

        total: int = db.execute(
            text("""
                SELECT COUNT(*) FROM loan_request
                WHERE first_name LIKE :first_name
                   OR last_name LIKE :last_name
            """),
            params
        ).scalar() or 0

        result = db.execute(
            text("""
                SELECT * FROM loan_request
                WHERE first_name LIKE :first_name
                   OR last_name LIKE :last_name
                LIMIT :limit OFFSET :offset
            """),
            {**params, "limit": limit, "offset": offset}
        ).fetchall()

        return {
            "data": [dict(row._mapping) for row in result],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }
    finally:
        db.close()


@tool
def show_by_email_or_phone(
    email: Optional[str] = None,
    phone: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> dict:
    """
    Fetch loan requests by email, phone number, or both using partial matching.
    Use this tool when you want to search loan requests by email or phone number.

    Args:
        email: The email address (or partial email) of the loan request holder.
        phone: The phone number (or partial phone number) of the loan request holder.
        limit: Maximum number of records to return (default 10, max 50).
        offset: Number of records to skip for pagination (default 0).

    Returns:
        Dict with 'data' (list of matching loan requests) and pagination info.
    """
    limit = min(limit, 50)

    db = next(get_b2b_db())
    try:
        params = {
            "email": f"%{email}%" if email else "%",
            "phone": f"%{phone}%" if phone else "%",
        }

        total: int = db.execute(
            text("""
                SELECT COUNT(*) FROM loan_request
                WHERE email LIKE :email
                   OR mobile LIKE :phone
            """),
            params
        ).scalar() or 0

        result = db.execute(
            text("""
                SELECT * FROM loan_request
                WHERE email LIKE :email
                   OR mobile LIKE :phone
                LIMIT :limit OFFSET :offset
            """),
            {**params, "limit": limit, "offset": offset}
        ).fetchall()

        return {
            "data": [dict(row._mapping) for row in result],
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }
    finally:
        db.close()