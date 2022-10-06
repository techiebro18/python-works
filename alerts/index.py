import mongo
import snowflake_module
import slack
from decouple import config

def get_mongo_products_count():
    dbname = mongo.get_database()
    collection_name = dbname['vb_products']
    return collection_name.count_documents({})
    
def get_snowflake_products_count():
    cursor = snowflake_module.get_cursor()
    rs = cursor.execute('select count(*) from vb_products')
    (num_rows,) = rs.fetchone()
    return num_rows


if __name__ == "__main__":
    mongo_count = get_mongo_products_count()
    snowflake_count = get_snowflake_products_count()
    if int(abs(mongo_count - snowflake_count)) > 100:
        html = f'We have difference in products of Mongo and Snowflake. Mongo Products: {mongo_count}, Snowflake Products: {snowflake_count}'
        slack.send_alert(text=html)
        print("Success!")
        
