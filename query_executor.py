import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from database_manager import engine

def execute_query(query):
    try:
        with engine.connect() as connection:
            result = pd.read_sql(query, connection)
        return result
    except SQLAlchemyError as e:
        return f"An error occurred while executing the query: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
