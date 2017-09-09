from dac import dac_code
from cust import customer_functions
from orders import order_code as order_code
from alexa_responce import responce_code

def create_newUser(userid):
    connection = dac_code.create_conn()
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `Customers` (`amazon_id`) VALUES (%s)"
            cursor.execute(sql, userid)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()


    finally:
        connection.close()


def checkforexistingcustomerorder(customerid):
    orderid = 0
    # get
    sqlcode = "SELECT orders.order_autoid  FROM fred.orders orders WHERE (orders.customerid = '" + str(
        customerid) + "') AND (orders.order_status_int = 0)"
    result = dac_code.dbreadquery_sql(sqlcode)
    custdict: dict ={}
    if len(result)==1:
        custdict=result[0]

    if custdict is None:
        # create a new order
        print("create new order")
        orderid = order_code.create_new_order(customerid)
    else:

        orderid = custdict.get('order_autoid')
        print("Found order id = " + str(orderid))

    return orderid


def find_customer_name(session_started_request, session):
    """ Called when the session starts """
    session_attributes = {}
    print("finding customer info")

    id = str(session['user'].get('userId'))
    userinfo = dac_code.dbreadquery(id)
    # check to see is userinfo is empty
    if userinfo is None:
        print("new user")
        customer_functions.create_newUser(id)
    else:
        print("ALL user info " + str(userinfo))
        username = userinfo.get('fname')
        print("THE userid " + str(id))
        print("THE username " + str(username))

    reprompt_text = "Did you get that?"
    should_end_session = False
    card_title = "Your name is"
    speech_output = "Your name is " + str(username)
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


