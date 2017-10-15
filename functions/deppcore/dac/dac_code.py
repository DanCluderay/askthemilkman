import pymysql.cursors
def create_conn():
    con = pymysql.connect(host='cluderay.clmxvwimtl0m.eu-west-1.rds.amazonaws.com',
                          user='cluderay',
                          password='cluderay',
                          db='fred',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    return con





def dbreadquery(userid):
    connection = create_conn()
    try:

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Customers.*, Customers.amazon_id  FROM fred.Customers Customers WHERE (Customers.amazon_id = '" + userid + "')"
            cursor.execute(sql)
            result = cursor.fetchone()
            print("customer details " + str(result))
            return result
    finally:
        connection.close()


def db_sql_write(sql):
    connection = create_conn()
    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql)
            connection.commit()

            return 1
    finally:
        connection.close()


def dbreadquery_sql(sql):
    connection = create_conn()
    try:
        with connection.cursor() as cursor:
            # Read a single record
            cursor.execute(sql)
            result = cursor.fetchall()
            connection.commit()
            print("customer details " + str(result))
            return result
    finally:
        connection.close()


def dbquery(orderstring):
    connection = create_conn()
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `test_orders` (`test`, `ordertest`) VALUES (%s, %s)"
            cursor.execute(sql, ('2', orderstring))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `test`, `ordertest` FROM `test_orders` WHERE 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
