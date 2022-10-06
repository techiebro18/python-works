import psycopg2
import matplotlib.pyplot as plt

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
    curr.execute(sql)
    results = curr.fetchmany(10) #Fetch only the number of rows passed as an argument
    users = []
    orders =[]
    for row in results:
        users.append(row[0])
        orders.append(row[1])

    #Visualizing Data
    plt.bar(users, orders)
    plt.ylim(0, 5)
    plt.xlabel("Users")
    plt.ylabel("Orders")
    plt.title("User orders")
    plt.show()

    curr.close()
except (Exception, psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
        print("Database Connection Closed!")
