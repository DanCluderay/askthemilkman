import pymysql.cursors
def create_conn():
    con = pymysql.connect(host='cluderay.clmxvwimtl0m.eu-west-1.rds.amazonaws.com',
                          user='cluderay',
                          password='cluderay',
                          db='bill',
                          charset='utf8mb4',
                          cursorclass=pymysql.cursors.DictCursor)
    return con



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
            return result
    finally:
        connection.close()


