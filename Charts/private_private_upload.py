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
    sql = '''
    select vu.email, count(*) from vintage_bar_live.vb_products vp 
left join vb_users vu on vp.commission_user_id = vu.id 
WHERE vp.commission_user_type = 'private' and vp.created_at >= '2021-01-01 00:00:00' 
and vu.email is not NULL and vu.status = 'active'
GROUP BY vu.email  
    '''
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    days = []
    products = []
    for item in myresult:
        days.append(item[0])
        products.append(item[1])

    plt.subplots_adjust(bottom=0.30)
    plt.xticks(rotation=85)
    plt.bar(days, products)
    #plt.ylim(0, 10)
    plt.xlabel("Users")
    plt.ylabel("Products")
    plt.title("Products uploaded by users")
    plt.show()

except Error as e:
    print(e)