import psycopg2
import matplotlib.pyplot as plt
import pandas as pd

try:
    con = psycopg2.connect(
        host = 'thevintagebar.cfq6jedl25zx.us-east-2.rds.amazonaws.com',
        database = 'postgres',
        user = 'postgres',
        password = 'TvB2018!'
    )

    cur = con.cursor()
    sql = '''with rows as
            (
                select oc.user_id, oc."timestamp", row_number() over (partition by oc.user_id order by oc."timestamp") as rn  
                from web_store_backend_prod.order_completed oc 
                left join personas_prod.users u on u.id = oc.user_id 
                where u.rfm_best_and_loyal_customers = true 
                group by oc.user_id, oc."timestamp" order by oc.user_id,oc."timestamp" asc 
            )
            select oc1.user_id, date_part('day', oc2.timestamp - oc1.timestamp) as duration
            from rows oc1
            join rows oc2
            on oc1.user_id = oc2.user_id 
            where oc1.rn < oc2.rn and oc2.rn = 2
            '''

    cur.execute(sql)
    rs = cur.fetchall()
    cur.close()
    
    df = pd.DataFrame(rs, columns=['user_id', 'duration'])
    df.head()
    #df.sort_values(by='days_since_last_transaction', ascending=True)
    categories = df['user_id']
    total_orders = df['duration']
    plt.subplots_adjust(bottom=0.30)
    plt.xticks(rotation=80, fontsize=8)
    plt.bar(categories, total_orders, label = 'Days')
    plt.xlabel("Users")
    plt.ylabel("Time Durations")
    plt.title("Duration in second orders")
    plt.legend()
    plt.show()


    plt.pie(total_orders,labels = categories, autopct = '%.2f%%')
    #plt.pie(total_orders,labels = categories, autopct = '%.2f%%', startangle=90)
    #plt.axis('equal')
    #plt.tight_layout()
    #plt.pie(total_orders,labels = categories, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
    plt.title('Duration in second orders')
    plt.legend()
    #plt.legend(total_orders, categories, loc="best")
    plt.show()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if con is not None:
        con.close()
        print("Database connection closed!")

