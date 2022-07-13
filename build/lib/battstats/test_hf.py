import battstats
import pandas as pd
from sqlalchemy import create_engine
from dotenv import dotenv_values


# Create test for lookup_id
 
# def test_lookup_id():
#     test_id = battstats.lookup_id(filter_val = "BG_MT_25R_ICT_Cell_3_Take2", 
#                                     target_table = "testdata_meta",
#                                     filter_col = "data_file")
#     print(test_id)
#     assert(test_id == 316)

#     schedule_id = battstats.lookup_id(filter_val = "BG_MT_25R_ICT_Cell_3_Take2",
#                                         target_table = "testdata_meta", 
#                                         filter_col = "data_file", 
#                                         table_id = "schedule_id")
#     assert(schedule_id == 117)

engine, conn = battstats.create_db_connection()
print(engine)