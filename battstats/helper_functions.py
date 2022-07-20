import numpy as np
import pandas as pd
from dotenv import dotenv_values
from sqlalchemy import create_engine
import psycopg2
import json
import logging
import os

logging.basicConfig(level=logging.DEBUG, 
                    filename='log.log', 
                    filemode='w', 
                    format='%(asctime)s %(name)s - %(levelname)s - %(message)s')

log = logging.getLogger(__name__)

def create_db_connection():
    '''
    Creates connection to database for the variables specified in the .env
    file in the directory.
    '''
    # Load DB configuration from .env file.
    # Exit if no configuration values found in .env.
    db_config = dotenv_values()
    if not db_config:
        log.error("Could not find .env values to connect to database.")
        return None, None

    TARGET = db_config['DB_TARGET']
    USER = db_config['DB_USERNAME']
    PW = db_config['DB_PASSWORD']
    HOST = db_config['DB_HOSTNAME']
    PORT = db_config['DB_PORT']

    # Create the engine
    engine = create_engine('postgresql+psycopg2://' + USER + ':' + PW + '@' + HOST + ':' + PORT + '/' + TARGET)
    connection = engine.connect()

    return engine, connection

def kill_connection(engine, conn):
    '''
    This function takes an engine and session and kills them both, once
    we're finished with them.

    Parameters
    ----------
    engine : SQLAqlchemy Engine
        The name of the engine to kill.
    engine : SQLAqlchemy session
        The name of the session to kills
    '''
    conn.close()
    engine.dispose()

def build_query_string(select_vals, target_table : str, where_col : str, where_val : str):
    '''
    Takes select, where and from values and combines them to create a string to be used
    as a SQL query.

    Parameters
    ----------
    select_vals : string/list
        Name of columns that to be extracted from database. In case of list, values
        are concatenated together.
    target_table : str
        Table where values are to be extracted from
    where_col : str
        Conditions to determine what rows are to be extracted from the database
    where_val : str
        Row values that the database is filtered to.

    Returns
    -------
    statement : string
        A string combining all of the input values into a SQL query.
    '''
    # Combines list of SELECT items into a single string
    if isinstance(select_vals, list):
        select = select_vals[0]
        for val in select_vals[1:]:
            select += ', ' + val
    else:
        select = select_vals
    
    # format strings so we don't run into issues with matching capitalization
    if isinstance(where_val, str):
        where_val = '\'' + where_val.lower() + '\''
        where_col = 'LOWER(' + where_col + ')' 
    else:
        where_val = str(where_val)

    statement = 'SELECT ' + select + ' FROM ' + target_table + ' WHERE ' + where_col + ' = ' + where_val + ';';
    return statement

def get_meta_variables(meta_variables, schedule_id : str):
    engine, conn = create_db_connection()

    query = build_query_string(meta_variables, 'schedules_meta', 'schedule_id', schedule_id)

    meta_values = pd.read_sql(query, conn)

    # Check that we've received meta values for one schedule
    if len(meta_values) == 0:
        log.error('Schedule ID: ' + str(schedule_id) + ' doesn\'t exist in schedules_meta')
        kill_connection(engine, conn)
        return None
    elif len(meta_values) > 1:
        log.error('Schedule ID: ' + str(schedule_id) + " returned more than one row from schdules_meta")
        kill_connection(engine, conn)
        return None

    # Converts table of meta values into dictionary
    meta_dict = {}
    for var in meta_variables:
        meta_dict[var] = meta_values[var][0]

    kill_connection(engine, conn)
    return meta_dict

def _create_config_dict(config_file):
    """
    Parses the config file and returns a read-only dictionary of test configuration infromationl.
    ----------
    config_file : String

    Returns
    -------
    config : ReadOnlyDict
        A read-only dictionary containing test configuartion information 
    """

    # Line in the Arbin CSV where the test name is saved. Maybe move this to a config at some point?
    test_name_line = 6

    if not os.path.exists(config_file):
        log.error("Path does not exist for test configuration file: " + config_file)
        return None
    else:
        with open(config_file, 'r') as file:
            dict = json.load(file)

    # Check to see if source file exists. Need to update this

    # if not os.path.exists(dict['source_path'] + dict['source_file']):
    #     log.error("Path does not exist for target file:  " + dict['source_path']  + dict['source_file'])
    #     return None

    return dict

def load_data(test_id, target_table):
    '''
    Takes a test id as input and returns all columns of the corresponding test.

    Parameters
    ----------
    test_id : int
        Primary key corresponding to desired test
    target_table : string
        Table to extract data from
    
    Returns
    -------
    data : pandas dataframe
        All columns matching test_id
    '''
    engine, conn = create_db_connection()
    query = build_query_string('*', target_table, 'test_id', test_id)
    data = pd.read_sql(query, conn)

    return data

def get_test_ids(test_name : str):
    '''
    Makes SQL query on testdata_meta and returns test_id and schedule_id for the
    test_name passed.

    Parameters
    ----------
    test_name : str
        Name of test 

    Returns
    -------
    lookup_ids : pandas dataframe
        Returns dataframe with [schedule_id, test_id] for the specified test_name.
    '''

    engine, conn = create_db_connection()

    # Build query string using passed variables and request values from database
    query = build_query_string(['schedule_id', 'test_id'], 'testdata_meta', 'data_file', test_name)
    lookup_ids = pd.read_sql(query, conn)
    
    # Make sure exactly one ID is returned
    if lookup_ids.shape[0] > 1:
        print('ID not unique.')
        kill_connection(engine, conn)
        return None
    elif lookup_ids.shape[0] == 0:
        log.error('testdata_meta does not contain an entry for ' + test_name + ' in the "data_file" column.')
        kill_connection(engine, conn)
        exit()
    
    kill_connection(engine, conn)
    return lookup_ids.astype(int)

test_id = get_test_ids("BG_AmBatt2_Cell7_ICT")['test_id'].values[0]
print(load_data(test_id, 'testdata_meta'))