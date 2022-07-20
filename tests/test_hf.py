import battstats
import pandas as pd
from sqlalchemy import create_engine
from dotenv import dotenv_values


# Create test for lookup_id
 
def test_get_test_ids():
    return

engine, conn = battstats.create_db_connection()
print(engine)