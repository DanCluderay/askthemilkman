import uuid
import dac_code
import customer_functions
import responce_code
from datetime import datetime, timedelta, time
import globalvars as gv
'''
from dac import dac_code
from cust import customer_functions
from alexa_responce import responce_code
from datetime import datetime, timedelta, time
from global_vars import globalvars as gv
'''

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

def deliver_my_order(intent, session):
    print("Intent " + str(intent))

    delivery_request = str(intent['slots']['delivery_date']['value'])
    return_date =  set_delivery_date(delivery_request)
    print("return date = " + str(return_date))
    update_order_delivery_date(return_date)

    return_text = "Great, we deliver it on " + str(return_date.strftime("%A") + " the " + str(return_date.date()))
    session_attributes = {}
    card_title = "Order Delivery"

    speech_output = return_text
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Did you get that?"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def update_order_delivery_date(delivery_date):
    CURRENT_ORDERID = customer_functions.checkforexistingcustomerorder(gv.CURRENT_USERID)

    sql = "UPDATE `orders` SET `delivery_date`='" + str(f"{delivery_date:%Y-%m-%d}") + "' WHERE order_autoid='" + str(
        CURRENT_ORDERID) + "'"
    print(sql)
    dac_code.db_sql_write(sql)
    print("perform a query on this order = " + str(CURRENT_ORDERID))

def set_delivery_date(when2):
    new_delivery_date = datetime.today()
    DAY_OF_WEEK_now = datetime.today().isoweekday()
    DESIRED_DAY_OF_WEEK = 0  # default value
    ACTUAL_DAY_OF_WEEK = 0  # the result variavble
    day_of_week_calc = 0
    ADD_DAYS = 0
    if when2.upper() == 'TOMORROW':
        ADD_DAYS = 1

    elif when2.upper() == 'ASAP':
        pass
    elif when2.upper() == 'AS SOON AS POSSIBLE':
        pass
    elif when2.upper() == 'THIS EVENING':
        action_date = datetime.now()
    elif when2.upper() == 'TOMORROW MORNING':
        ADD_DAYS = 1
    elif when2.upper() == 'TOMORROW EVENING':
        ADD_DAYS = 1
    elif when2.upper() == 'SUNDAY':

        DESIRED_DAY_OF_WEEK = 7
        day_of_week_calc = 1
    elif when2.upper() == 'MONDAY':

        DESIRED_DAY_OF_WEEK = 1
        day_of_week_calc = 1
    elif when2.upper() == 'TUESDAY':

        DESIRED_DAY_OF_WEEK = 2
        day_of_week_calc = 1
    elif when2.upper() == 'WEDNESDAY':

        DESIRED_DAY_OF_WEEK = 3
        day_of_week_calc = 1
    elif when2.upper() == 'THURSDAY':

        DESIRED_DAY_OF_WEEK = 4
        day_of_week_calc = 1
    elif when2.upper() == 'FRIDAY':

        DESIRED_DAY_OF_WEEK = 5
        day_of_week_calc = 1
    elif when2.upper() == 'SATURDAY':

        DESIRED_DAY_OF_WEEK = 6
        day_of_week_calc = 1
    else:
        return 0

    if day_of_week_calc == 1:

        # work out howmany days to add on
        if DAY_OF_WEEK_now > DESIRED_DAY_OF_WEEK:
            # add 7 days to desired day
            DESIRED_DAY_OF_WEEK = DESIRED_DAY_OF_WEEK + 7

        ACTUAL_DAY_OF_WEEK = (DESIRED_DAY_OF_WEEK - DAY_OF_WEEK_now)
        new_delivery_date = datetime.now() + timedelta(days=ACTUAL_DAY_OF_WEEK)

    else:
        new_delivery_date = datetime.now() + timedelta(days=ADD_DAYS)

    return new_delivery_date


def add_something_to_an_order(intent, session):
    # find what varient they mean? - e.g if they say weetabix, or milk what size and type to they mean.a
    session_attributes = {}
    print("Adding something to my order")
    customerid = 0
    id = str(session['user'].get('userId'))

    # get the customer info
    sql = "SELECT Customers.* FROM fred.Customers Customers WHERE (Customers.amazon_id = '" + str(id) + "')"
    print("sql of customer query " + sql)
    results:dict = dac_code.dbreadquery_sql(sql)
    print("theresults " + str(results))
    customercount=0
    customer_dict:dict={}
    for listofcustomer in results:
        customercount=customercount+1
        customer_dict=listofcustomer
    if customercount==0:
        print("we cannot find a customer")
    else:
        customerid = customer_dict.get('customers_autoid')

    # is there an order already? if not create one
    orderid = customer_functions.checkforexistingcustomerorder(customerid)

    # find out the product details
    # first find out the product type
    print("INTENT - " + str(intent))

    # add items to order
    productname = str(intent['slots']['product']['value'])
    sql = "INSERT INTO `order_items` (`oitems_orderid`, `order_date`, `Items_product_id`, `item_description`, `items_cost_ex_vat`, `vatcode`, `qty`) VALUES ('" + str(
        orderid) + "', '" + str('2017-01-01 00:00:00') + "', '1', '" + str(productname) + "', '0.075', '1', '1')"
    # print("insert new order sql - " + sql)
    dac_code.db_sql_write(sql)

    reprompt_text = "Did you get that?"
    should_end_session = False
    card_title = "We've added something to your order"
    speech_output = "We've added something to your order"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
