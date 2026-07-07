from langchain.tools import tool
from dotenv import load_dotenv
from sqlalchemy import text, inspect
from database.connection import get_b2b_db
from langchain.tools import tool

load_dotenv()

@tool
def show_tables():
    """
    This tool will be used to show all the tables from the database. This will execute basically get tables from the database and
    give the list of the tables from the retrived data
    """

    db = next(get_b2b_db())
    try:
        engine = db.get_bind()
        inspector = inspect(engine)
        return {
            "tables":inspector.get_table_names()
        }
    finally:
        db.close()

@tool
def table_details(table:str):
    """
    This tool will help in fetching the details of passed table.
    Following details this tool will provide
    1. Columns of the table
    2. Primary key constraint
    3. Foreignkeys of the table
    4. Indexes of the table
    Arg:
        table: name of the table whose metadata to be fetched
    Response:
        Dictionary of the details as mentioned in the description
    """
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

@tool
def select_query_executor(query:str):
    """
    This tool will be used for all select queries that must be run on the database.
    Arg:
        query: Only SQL SELECT query with conditions and other aspects to fetch the data
    Response:
        dictionary with results in the key result
    """

    db = next(get_b2b_db())

    try:
        result = db.execute(text(query))
        return {
            "result":[dict(row._mapping) for row in result]
        }
    finally:
        db.close()