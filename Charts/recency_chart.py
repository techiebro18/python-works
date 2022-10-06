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
    sql = '''with
    first_transaction as (
        select  u.email, DATE_PART('day', current_date::timestamp - min(oc.received_at)::timestamp) as first
          from  web_store_backend_prod.order_completed oc
     left join  web_store_backend_prod.users u
            on  oc.user_id = u.id
         where  oc.received_at > (current_date - interval '6 month')
      group by  1
    ),
    frequency as (
        select  u.email,
                count(distinct oc.order_id) as frequency
          from  web_store_backend_prod.order_completed oc
     left join  web_store_backend_prod.users u
            on  oc.user_id = u.id
         where  oc.received_at > (current_date - interval '6 month')
      group by  1
    ),
    last_transaction as (
        select  u.email,
                DATE_PART('day', current_date::timestamp - max(oc.received_at)::timestamp) as last
          from  web_store_backend_prod.order_completed oc
     left join  web_store_backend_prod.users u
            on  oc.user_id = u.id
         where  oc.received_at > (current_date - interval '6 month')
      group by  1
    ), 
    average_transaction_size as (
        select  u.email,
                avg(oc.total) as avg
          from  web_store_backend_prod.order_completed oc
     left join  web_store_backend_prod.users u
            on  oc.user_id = u.id
         where  oc.received_at > (current_date - interval '6 month')
      group by  1
      order by  2 desc
    )
        select  distinct 
                u.email,
                COALESCE(f.frequency, 0) as frequency,
                COALESCE(z.last, 0) as days_since_last_transaction,
                COALESCE(a.first, 0) as days_since_first_transaction,
                round(t.avg, 2) as average_transaction_size
          from  web_store_backend_prod.users u
     left join  first_transaction a
            on  u.email = a.email
     left join  frequency f
            on  u.email = f.email
     left join  last_transaction z
            on  u.email = z.email
     left join  average_transaction_size t
            on  u.email = t.email
     where z.last > 0
      order by  3 asc limit 100'''

    cur.execute(sql)
    rs = cur.fetchmany(50)
    cur.close()
    
    df = pd.DataFrame(rs, columns=['email', 'frequency', 'days_since_last_transaction', 'days_since_first_transaction', 'average_transaction_size'])
    df.head()
    #df.sort_values(by='days_since_last_transaction', ascending=True)
    emails = df['email']
    last_transactions = df['days_since_last_transaction'].sort_values(ascending=True)
    plt.subplots_adjust(bottom=0.30)
    plt.xticks(rotation=60, fontsize=6)
    plt.bar(emails, last_transactions, label = 'Days')
    plt.xlabel("Users")
    plt.ylabel("Days since last transaction")
    plt.title("User with Number of days since last transaction")
    plt.legend()
    plt.show()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if con is not None:
        con.close()
        print("Database connection closed!")

