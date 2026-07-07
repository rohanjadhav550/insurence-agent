from langchain.tools import tool
from dotenv import load_dotenv
from sqlalchemy import text, inspect
from database.connection import get_b2b_db

load_dotenv()

def database_tables_scann_tool():
    """
    This tool will be helpfull in finding the tables, there descriptions and details present in the database.
    Use this tool for the details about the database
    """

    try:
        # Get the list of the tables
        tables = show_tables()
        
        for table in tables:
            # get details of each table
            details = table_details(table)
            print(details)
            print()
    finally:
        print()

def show_tables():
    db = next(get_b2b_db())
    try:
        engine = db.get_bind()
        inspector = inspect(engine)
        return inspector.get_table_names()
    finally:
        db.close()

def table_details(table):
    db = next(get_b2b_db())
    try:
        engine = db.get_bind()
        inspector = inspect(engine)
        
        # columns of the table
        columns = inspector.get_columns(table)

        # primary key 
        pk = inspector.get_pk_constraint(table)

        # foreign key constraints
        fks = inspector.get_foreign_keys(table)

        # indexes
        index = inspector.get_indexes(table)

        return {
            "columns": columns,
            "primary_key": pk,
            "foreign_keys": fks,
            "indexes": index
        }
    finally:
        db.close()    

database_tables_scann_tool()