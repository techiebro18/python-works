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
    sql = '''with order_completed as (
            select distinct (elements->>'product_id')::numeric product_id, oc.user_id, oc.order_id, oc.products
            from web_store_backend_prod.order_completed oc, json_array_elements(oc.products::json) elements
        ), unique_product as (
            select distinct(pv.product_id), pv.category from thevintagebarcomprod.product_added pv 
        )
        select distinct(pc2.category) as categories, count(*) as total_orders 
        from personas_prod.users u
        left join order_completed oc on oc.user_id = u.id 
        left join unique_product pc2 on pc2.product_id = oc.product_id::text 
        where rfm_best_and_loyal_customers = true and pc2.category is not null 
        and upper(pc2.category) = pc2.category
        group by pc2.category order by 2 desc'''

    cur.execute(sql)
    rs = cur.fetchall()
    cur.close()
    
    df = pd.DataFrame(rs, columns=['categories', 'total_orders'])
    df.head()
    #df.sort_values(by='days_since_last_transaction', ascending=True)
    categories = df['categories']
    total_orders = df['total_orders']
    plt.subplots_adjust(bottom=0.30)
    plt.xticks(rotation=60, fontsize=8)
    plt.bar(categories, total_orders, label = 'Orders')
    plt.xlabel("Categories")
    plt.ylabel("Orders")
    plt.title("Categories with total orders")
    plt.legend()
    plt.show()


    plt.pie(total_orders,labels = categories, autopct = '%.2f%%')
    #plt.pie(total_orders,labels = categories, autopct = '%.2f%%', startangle=90)
    #plt.axis('equal')
    #plt.tight_layout()
    #plt.pie(total_orders,labels = categories, autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
    plt.title('Categories with total orders')
    plt.legend()
    #plt.legend(total_orders, categories, loc="best")
    plt.show()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if con is not None:
        con.close()
        print("Database connection closed!")

