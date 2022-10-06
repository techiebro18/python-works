from snowflake import connector
from decouple import config

def get_cursor(**kwargs):
    conn = connector.connect(
                user=config('SN_USER'),
                password=config('SN_PASSWORD'),
                account=config('SN_ACCOUNT'),
                warehouse=config('SN_WAREHOUSE'),
                database=config('SN_DATABASE'),
                schema=config('SN_SCHEMA')
                )
    cursor = conn.cursor()
    return cursor

    
        
