from __future__ import print_function
import pymysql.cursors
import json
import boto3
import uuid
from datetime import datetime, timedelta, time
import shopify

CURRENT_USERID = 0
CURRENT_ORDERID = 0


# this
# Connect to the database
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
            result = cursor.fetchone()
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


def create_newUser(userid):
    connection = create_conn()
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


def create_customer_job(customerid, product, qty, size, task_type, taskdate, originalquote):
    connection = create_conn()
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `test_orders` (`test`, `ordertest`) VALUES (%s, %s)"
            #cursor.execute(sql, ('2', orderstring))

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


def mq(v):
    client = boto3.client('iot-data', region_name='eu-west-1', aws_access_key_id='AKIAJ35UPJ3TR23R56XA',
                          aws_secret_access_key='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')
    response = client.publish(
        topic='dancluderay',
        qos=1,
        payload=json.dumps({"msg": v})

    )


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Session Started"
    speech_output = "Welcome to the milkman"

    reprompt_text = "Please tell me what you would like to order and when you would like it delivered"

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using your local milkman" \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_shopping_list_attributes(stuff):
    return {"shoppinglist": stuff}


def place_order_and_deliver(intent, session):
    print("place order and deliver calue " + str(intent))

    session_attributes = {}
    card_title = "Order Delivery"
    speech_output = "Yes, i can deliver your order now"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Did you get that?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def how_much_is_my_order(intent, session):
    print("This is the cost " + str(intent) + " to the order")

    session_attributes = {}
    card_title = "Your Shopping list"
    speech_output = "Youve spent £10 this week"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Did you get that?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def whats_on_my_shopping_list(intent, session):
    print("whats_on_my_shopping_list " + str(intent) + " to the order")

    session_attributes = {}
    card_title = "Your Shopping list"
    speech_output = "I've 10 things on your shopping list"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Did you get that?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def add_item_to_order(intent, session):
    print("Ive added " + str(intent) + " to the order")

    session_attributes = {}
    card_title = "I've added milk to your order"
    speech_output = "I've added milk to your order"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Did you get that?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def placeanorder(intent, session, productsize, whentodeliver, delivery_or_add, producttype, howmany):
    print("Ive added " + str(intent) + " to the order")

    session_attributes = {}
    card_title = "I've added milk to your order"

    s_howmany: str = ''
    if howmany == '1' or str(howmany) == 'a':
        s_howmany = 'a'
    else:
        s_howmany = str(howmany)

    s_deliverwhen: str = ''
    if str(whentodeliver) == 'Monday':
        s_deliverwhen = 'on Monday'
    elif str(whentodeliver) == 'Tuesday':
        s_deliverwhen = 'on Tuesday'
    elif str(whentodeliver) == 'Wednesday':
        s_deliverwhen = 'on Wednesday'
    elif str(whentodeliver) == 'Thursday':
        s_deliverwhen = 'on Thursday'
    elif str(whentodeliver) == 'Friday':
        s_deliverwhen = 'on Friday'
    elif str(whentodeliver) == 'Saturday':
        s_deliverwhen = 'on Saturday'
    elif str(whentodeliver) == 'Sunday':
        s_deliverwhen = 'on Sunday'
    else:
        s_deliverwhen = str(whentodeliver)

    speech_output = "Great, we'll " + str(delivery_or_add) + " " + s_howmany + " " + str(
        productsize) + " bottle of " + str(producttype) + " " + str(whentodeliver)
    # mq(speech_output)
    print('about to go to db')
    dbquery(speech_output)
    print(speech_output)

    reprompt_text = "Did you get that?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("Hey there")
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
    id = str(session['user'].get('userId'))
    userinfo = dbreadquery(id)
    # check to see is userinfo is empty
    if userinfo is None:
        print("new user")
        create_newUser(id)
        userinfo = dbreadquery(id)

    print("user info" + str(userinfo))
    username = userinfo.get('fname')
    print("the userid" + str(id))
    print("the userid" + str(username))
    CURRENT_USERID = int(str(userinfo.get('customers_autoid')))


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    # mqttmsg()
    return get_welcome_response()


def on_intent(intent_request, session, context):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    hasallpart = True
    intent = intent_request['intent']
    print(intent)
    intent_name = intent_request['intent']['name']

    if intent_name == "MakeAnOrder":
        sl = intent_request['intent']['slots']
        print("slots: " + str(sl))
        # l='{"name": "MakeAnOrder", "slots": {"productsize": {"name": "productsize", "value": "4 pint"}, "WhenToDeliver": {"name": "WhenToDeliver", "value": "now"}, "DeliverOrAdd": {"name": "DeliverOrAdd", "value": "deliver"}, "addmilk": {"name": "addmilk", "value": "whole milk"}, "howmany": {"name": "howmany", "value": "1"}}}'
        lp = json.dumps(sl)
        json1_data = json.loads(str(lp))
        print("unknown - " + str(json1_data))
        productsize: str = ''
        whentodeliver: str = ''
        delivery_or_add: str = ''
        producttype: str = ''
        howmany: str = ''

        # can we loop the dict here?
        for key, val in json1_data.items():
            print("{} = {}".format(key, val))

        if len(json1_data["productsize"]["value"]) > 0:
            productsize = str(json1_data["productsize"]["value"])

        if len(json1_data["WhenToDeliver"]["value"]) > 0:
            whentodeliver = str(json1_data["WhenToDeliver"]["value"])

        if len(json1_data["DeliverOrAdd"]["value"]) > 0:
            delivery_or_add = str(json1_data["DeliverOrAdd"]["value"])

        if len(json1_data["addmilk"]["value"]) > 0:
            producttype = str(json1_data["addmilk"]["value"])

        if len(json1_data["howmany"]["value"]) > 0:
            howmany = str(json1_data["howmany"]["value"])

        hasallpart: bool = False
        if len(productsize) > 0 and len(whentodeliver) > 0 and len(delivery_or_add) > 0 and len(
                producttype) > 0 and len(
            howmany) > 0:
            hasallpart = True

        return placeanorder(intent, session, productsize, whentodeliver, delivery_or_add, producttype, howmany)
    elif intent_name == "WhatsOnMyShoppingList":
        return whats_on_my_shopping_list(intent, session)
    elif intent_name == "MakeAnOrder" and intent_name == "DeliverMyOrder":
        print("order and deliver triggered")
        return place_order_and_deliver(intent, session)
    elif intent_name == "AddToAnOrder":
        # return get_welcome_response()
        print("adding somthing to an order")
        return add_something_to_an_order(intent, session)
    elif intent_name == "WhatsMyName":
        # return get_welcome_response()
        print("calling finding customer name")
        return find_customer_name(intent, session)
    elif intent_name == "DeliverMyOrderOn":
        return deliver_my_order(intent, session)
    elif intent_name == "HowMuchIsMyOrder":
        return how_much_is_my_order(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" + event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'], context)
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def find_customer_name(session_started_request, session):
    """ Called when the session starts """
    session_attributes = {}
    print("finding customer info")

    id = str(session['user'].get('userId'))
    userinfo = dbreadquery(id)
    # check to see is userinfo is empty
    if userinfo is None:
        print("new user")
        create_newUser(id)
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
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_new_order(customerid):
    neworderid = 0
    guid = str(uuid.uuid4())
    connection = create_conn()
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `orders` (`customerid`, `GUID`,`order_status_int`,`order_status`) VALUES (" + str(
                customerid) + ", '" + str(guid) + "',0,'BUILDING')"
            print("insert new order sql - " + sql)
            db_sql_write(sql)
            sql = "SELECT orders.order_autoid  FROM fred.orders orders WHERE (orders.GUID = '" + str(guid) + "')"
            print("get order id sql - " + sql)
            result = dbreadquery_sql(sql)

            if result is None:
                # create a new order
                print("ccould not create an order")
            else:

                neworderid = result.get('order_autoid')
    finally:
        connection.close()
    return neworderid


def checkforexistingcustomerorder(customerid):
    orderid = 0
    # get
    sqlcode = "SELECT orders.order_autoid  FROM fred.orders orders WHERE (orders.customerid = " + str(
        customerid) + ") AND (orders.order_status_int = 0)"
    result = dbreadquery_sql(sqlcode)

    if result is None:
        # create a new order
        print("create new order")
        orderid = create_new_order(customerid)
    else:

        orderid = result.get('order_autoid')
        print("Found order id = " + str(orderid))

    return orderid


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


def deliver_my_order(intent, session):
    print("Intent " + str(intent))

    delivery_request = str(intent['slots']['delivery_date']['value'])
    return_date = set_delivery_date(delivery_request)
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
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def update_order_delivery_date(delivery_date):
    orderid = checkforexistingcustomerorder(CURRENT_USERID)

    sql = "UPDATE `orders` SET `delivery_date`='" + str(f"{delivery_date:%Y-%m-%d}") + "' WHERE order_autoid='" + str(
        orderid) + "'"
    print(sql)
    db_sql_write(sql)
    print("perform a query on this order = " + str(orderid))


def add_something_to_an_order(intent, session):
    # find what varient they mean? - e.g if they say weetabix, or milk what size and type to they mean.a
    session_attributes = {}
    print("Adding something to my order")
    customerid = 0
    id = str(session['user'].get('userId'))

    # get the customer info
    sql = "SELECT Customers.* FROM fred.Customers Customers WHERE (Customers.amazon_id = '" + str(id) + "')"
    results = dbreadquery_sql(sql)
    if results is None:
        print("we cannot find a customer")
    else:
        customerid = results.get('customers_autoid')

    # is there an order already? if not create one
    orderid = checkforexistingcustomerorder(customerid)

    # find out the product details
    # first find out the product type
    print("INTENT - " + str(intent))

    # add items to order
    productname = str(intent['slots']['product']['value'])
    sql = "INSERT INTO `order_items` (`oitems_orderid`, `order_date`, `Items_product_id`, `item_description`, `items_cost_ex_vat`, `vatcode`, `qty`) VALUES ('" + str(
        orderid) + "', '" + str('2017-01-01 00:00:00') + "', '1', '" + str(productname) + "', '0.075', '1', '1')"
    # print("insert new order sql - " + sql)
    db_sql_write(sql)

    reprompt_text = "Did you get that?"
    should_end_session = False
    card_title = "We've added something to your order"
    speech_output = "We've added something to your order"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

