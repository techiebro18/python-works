import psycopg2

try:
    conn = psycopg2.connect(
        host="thevintagebar.cfq6jedl25zx.us-east-2.rds.amazonaws.com",
        database="postgres",
        user="postgres",
        password="TvB2018!"
    )

    curr = conn.cursor()
    print("PostgreSQL Database Version")
    
    sql = 'select oc.user_id, oc.order_id, oc.received_at from web_store_backend_prod.order_completed oc limit 100'
    #curr.execute('SELECT version()')
    #db_version = curr.fetchone()
    curr.execute(sql)
    #results = curr.fetchall() #Fetch all records from the table
    results = curr.fetchmany(10) #Fetch only the number of rows passed as an argument
    for row in results:
        print("User Id:", row[0], end=" ")
        print("Order Id:", row[1], end=" ")
        print("Date:", row[2])

    #print(results)

    curr.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print("Database Connection Closed!")
