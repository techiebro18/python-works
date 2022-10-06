import matplotlib.pyplot as plt
from mysql.connector import connect, Error

try:
    mydb = connect(
            host = "tvb-production-mysql.cfq6jedl25zx.us-east-2.rds.amazonaws.com",
            user = "admin",
            password = "TvBLive2021!",
            database = "vintage_bar_live"
        )
    mycursor = mydb.cursor()
    sql = '''SELECT count(DISTINCT vp.name), DATE_FORMAT(voi.created_at, '%Y-%m-%d') as created_date from vb_order_items voi 
left join vb_products vp on vp.id = voi.product_id 
left JOIN vb_users vu on vu.id = vp.commission_user_id 
WHERE vp.commission_user_type = 'private' and vp.created_at >= '2021-01-01 00:00:00' and voi.status != 'pending'
GROUP BY created_date'''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    days = []
    products = []
    for item in myresult:
        days.append(item[1])
        products.append(item[0])

    plt.subplots_adjust(bottom=0.30)
    plt.xticks(rotation=85)
    plt.bar(days, products)
    #plt.ylim(0, 10)
    plt.xlabel("Days")
    plt.ylabel("Products")
    plt.title("Products sold each day")
    plt.show()

except Error as e:
    print(e)