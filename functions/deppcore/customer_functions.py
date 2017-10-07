import dac_code
import customer_functions
import order_code as order_code
import responce_code



def check_if_customer_address_exists_shopifyID(Customer_Address_shopifyid):
    sqlcode: str = "SELECT Customer_Addresses.shopify_address_id  FROM fred.Customer_Addresses Customer_Addresses WHERE (Customer_Addresses.CustomerID = " + str(Customer_Address_shopifyid) + ")"
    returnValue:bool=False
    result = dac_code.dbreadquery_sql(sqlcode)
    if len(result) > 0:
        returnValue= True # we have a result
    return returnValue

def check_if_customer_exists_email(email):
    sqlcode: str = "SELECT Customers.email  FROM fred.Customers Customers WHERE (Customers.email = '" + email + "' )"
    returnValue: bool = False
    result = dac_code.dbreadquery_sql(sqlcode)
    if len(result) > 0:
        returnValue = True  # we have a result
    return returnValue


def check_if_customer_exists_shopify_customerid(shopify_userid):
    sqlcode: str = "SELECT Customers.email  FROM fred.Customers Customers WHERE (Customers.shopify_userid = " + str(shopify_userid) + " )"
    returnValue: bool = False
    result = dac_code.dbreadquery_sql(sqlcode)
    if len(result) > 0:
        returnValue = True  # we have a result

    return returnValue

def get_internal_userid(intent, session):
    id = str(session['user'].get('userId'))
    val = 'accessToken' in session['user']
    if val == True:
        # we have a token for this customer - store it
        accessT = str(session['user'].get('accessToken'))

    print('is userid in dict' + str(val))
    #se = Singleton()
    #se.set_amazon_userid(id)
    userinfo = dac_code.dbreadquery(id)
    # check to see is userinfo is empty
    if userinfo is None:
        print("new user")
        customer_functions.create_newUser(id)

        userinfo = dac_code.dbreadquery(id)

    print("user info" + str(userinfo))
    username = userinfo.get('fname')
    print("the userid" + str(id))
    print("the userid" + str(username))
    tempnum = int(str(userinfo.get('customers_autoid')))
    #se.set_internal_userid(tempnum)
    return tempnum

def get_customer_current_order_number_from_id(customerid):
    #get the latest order details from a customer
    sqlcode: str = ''
    sqlcode = "SELECT orders.order_autoid FROM fred.orders orders WHERE orders.customerid = " + str(customerid) + " ORDER BY orders.orders_date DESC limit 1"
    result = dac_code.dbreadquery_sql(sqlcode)
    orderid: int = 0
    orderdict: dict = {}
    if len(result) == 1:  # we have a result
        orderdict = result[0]
        # we need to run an update command
        orderid = orderdict.get('order_autoid')

    return orderid

def get_customer_current_order(customerid):
    #get the latest order details from a customer
    sqlcode: str = ''
    sqlcode = "SELECT orders.customerid, orders.order_autoid,DATE_FORMAT(orders.delivery_date, '%Y-%m-%d %T.%f') as delivery_date, DATE_FORMAT(orders.orders_date, '%Y-%m-%d %T.%f') as orders_date, orders.ordervalue, orders.order_status, orders.order_status_int, orders.GUID, orders.delivery_status, orders.delivery_address_Line1, orders.delivery_address_Line2, orders.delivery_address_City, orders.delivery_address_Town, orders.delivery_address_Postcode, orders.delivery_address_Country, orders.Customer_First_Name, orders.CustomerTitle, orders.Customer_Second_Name, orders.ORDERID FROM fred.orders orders WHERE orders.customerid = " + str(
        customerid) + " ORDER BY orders.orders_date DESC limit 1"

    #sqlcode = "SELECT orders.customerid, orders.order_autoid, orders.ordervalue, orders.order_status, orders.orders_date, orders.order_status_int, orders.GUID, orders.delivery_status, orders.delivery_address_Line1, orders.delivery_address_Line2, orders.delivery_address_City, orders.delivery_address_Town, orders.delivery_address_Postcode, orders.delivery_address_Country, orders.Customer_First_Name, orders.CustomerTitle, orders.Customer_Second_Name, orders.delivery_date, orders.ORDERID FROM fred.orders orders WHERE orders.customerid = " + str(customerid) + " ORDER BY orders.orders_date DESC limit 1"
    result = dac_code.dbreadquery_sql(sqlcode)
    print(sqlcode)
    print(result)
    return result

def get_customer_order_items(orderid):
    #get the item details of an order
    sqlcode: str = ''
    sqlcode = "SELECT order_items.order_items_autoid,order_items.DealRetail, order_items.oitems_orderid, order_items.Items_product_varientid, order_items.item_description, order_items.items_cost_ex_vat, order_items.vatcode, order_items.qty FROM fred.order_items order_items WHERE (order_items.oitems_orderid = " + str(
        orderid) + ")"

    #sqlcode = "SELECT order_items.order_items_autoid, order_items.oitems_orderid, order_items.order_date, order_items.Items_product_varientid, order_items.item_description, order_items.items_cost_ex_vat, order_items.vatcode, order_items.qty FROM fred.order_items order_items WHERE (order_items.oitems_orderid = " + str(orderid) + ")"
    result = dac_code.dbreadquery_sql(sqlcode)
    print(sqlcode)
    print(result)
    return result

def get_all_customers(shopid):
    #checkif this customer is registered already
    sqlcode: str = ''
    sqlcode = "SELECT * FROM fred.Customers Customers WHERE 1"
    result = dac_code.dbreadquery_sql(sqlcode)
    print(sqlcode)
    print(result)
    return result

def check_customer_by_amazonid(amazonid):
    #checkif this customer is registered already
    sqlcode: str = ''
    sqlcode = "SELECT Customers.customers_autoid FROM fred.Customers Customers WHERE Customers.amazon_id = '" + amazonid + "'"
    result = dac_code.dbreadquery_sql(sqlcode)
    customerid:int=0
    custdict:dict={}
    if len(result) == 1:  # we have a result
        custdict = result[0]
        #we need to run an update command
        customerid=custdict.get('customers_autoid')

    return customerid

def update_customer_auth_token(userid, authcode):
    sqlcode="UPDATE COMMAND"
    pass

def get_customer_details(alexaid,userid):
    '''gets customer postcode and shop returned in the form of a dict'''
    customerpostcode:str=''
    sqlcode:str=''
    if alexaid != '' :
        print("Lookup by alexaid")
        sqlcode = "SELECT Customers.postcode, Customers.localshop  FROM fred.Customers Customers WHERE Customers.amazon_id = '" + alexaid+ "'"
    else:
        print("Lookup by userid")
        sqlcode = "SELECT Customers.postcode, Customers.localshop  FROM fred.Customers Customers WHERE Customers.customers_autoid = " + userid + ""

    result = dac_code.dbreadquery_sql(sqlcode)
    custdict: dict = {}
    if len(result) == 1:  # we have a result
        custdict = result[0]
        customerpostcode = custdict.get('postcode')
    else:
        # we dont have a result - we dont know this amazon device
        pass
    return custdict  # bail out


def check_postcode_is_covered(customerpostcode):
    deliverypossible:bool=False
    if customerpostcode == '':
        print('We do not have the customers postcode')
        return "I'm sorry we dont have your postcode, please enter it on the website"  # bail out
    else:
        print('check if the postcode if one we cover and by which shop')
        sqlcode="SELECT postcode_mapper.pc_autoid, postcode_mapper.postcode, postcode_mapper.coveringshop FROM fred.postcode_mapper postcode_mapper WHERE (postcode_mapper.postcode LIKE '" +customerpostcode + "%')"
    result = dac_code.dbreadquery_sql(sqlcode)
    custdict: dict = {}
    if len(result) == 1:  # we have a result we deliver to your address
        custdict = result[0]
        coveringshop = custdict.get('coveringshop')
        deliverypossible=True

    return deliverypossible

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
        card_title, speech_output, reprompt_text, should_end_session),authenticate=False)


