import uuid
from dac import dac_code

def create_new_order(customerid):
    neworderid = 0
    guid = str(uuid.uuid4())
    connection = dac_code.create_conn()
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `orders` (`customerid`, `GUID`,`order_status_int`,`order_status`) VALUES (" + str(
                customerid) + ", '" + str(guid) + "',0,'BUILDING')"
            print("insert new order sql - " + sql)
            dac_code.db_sql_write(sql)
            sql = "SELECT orders.order_autoid  FROM fred.orders orders WHERE (orders.GUID = '" + str(guid) + "')"
            print("get order id sql - " + sql)
            result = dac_code.dbreadquery_sql(sql)

            if result is None:
                # create a new order
                print("ccould not create an order")
            else:

                neworderid = result.get('order_autoid')
    finally:
        connection.close()
    return neworderid


