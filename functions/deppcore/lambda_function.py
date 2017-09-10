#!/usr/bin/python
# Filename: mymodule.py
from __future__ import print_function

import json

import pymysql.cursors
import boto3
import uuid
from datetime import datetime, timedelta, time
import shopify
from phpserialize import serialize, unserialize
import requests
import ast
import deepcore
#from .dacc import dac_code as dac #datacontroller

import dac_code
#from cust import customer_functions
import customer_functions as customer_functions
import responce_code
import alexa_intent_function_code  as aifc
import globalvars as gv
import local_shopify_code as l_shopify
import customer_functions as cust
#from orders import order_code as order_code
import order_code

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

        return aifc.placeanorder(intent, session, productsize, whentodeliver, delivery_or_add, producttype, howmany)
    elif intent_name=="connectalexa":
        print('running connectalexa...')

    elif intent_name == "WhatsOnMyShoppingList":
        print("somthing")
    elif intent_name == "CreateOrder":
        print("creating order")
        return l_shopify.Create_Order()
    elif intent_name == "OrderDelivered":
        print("creating order")
        return l_shopify.Create_Order()
    elif intent_name == "MakeAnOrder" and intent_name == "DeliverMyOrder":
        print("order and deliver triggered")
        return aifc.place_order_and_deliver(intent, session)
    elif intent_name == "whatsonmyorder":
        # return get_welcome_response()
        print("find out what is on the order")
        return add_something_to_an_order(intent, session)
    elif intent_name == "AddToAnOrder":
        # return get_welcome_response()
        print("adding somthing to an order")
        return add_something_to_an_order(intent, session)
    elif intent_name == "WhatsMyName":
        # return get_welcome_response()
        print('user intent: ' + str(intent))
        print('user session: ' + str(session))
        print("calling finding customer name")
        return cust.find_customer_name(intent, session)
    elif intent_name == "DeliverMyOrderOn":
        #order_code.deliver_my_order()
        return order_code.deliver_my_order(intent, session)
    elif intent_name == "HowMuchIsMyOrder":
        return aifc.how_much_is_my_order(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

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
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using your local milkman" \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return responce_code.build_response({}, responce_code.build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_shopping_list_attributes(stuff):
    return {"shoppinglist": stuff}






# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("Hey there")
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
    id = str(session['user'].get('userId'))
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
    CURRENT_USERID = int(str(userinfo.get('customers_autoid')))
    #CURRENT_ORDERID = checkforexistingcustomerorder(CURRENT_USERID)

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    # mqttmsg()
    return get_welcome_response()





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
    print('MAIN EVENT: ' + str(event))
    print('MAIN CONTEXT: ' + str(context))
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

#cust.find_customer_name('intent', 'session')
#order_code.create_new_order(123)

#dc.anotherthing()
#proccess_collections()
#create_new_customer_collection()
#checkforexistingcustomerorder("gggamzn1.ask.account.AGBI6UIAJIORPZLCDVIAOACMXHGO4IPHYPWTDZJSA4ASWDOXFBEV25F2UAH4OIXX2UXYZMMBP5ZMPETMAPA6CFUCTRXCKS6JZOQBOZ3YU2XOMEIPI6EMZYOT4KKHVK6XCJYS32ONDHTULJXJK5E3CVN4TU4E2WSCNMPUJBGY4MAV7ZOBJJEFM32IFJJLVSJJLKA24TGWSTVTIJA")
'''
#get a session key
sessk=pay_auth()
#tokenise a card - return a token cardid
cardid=sage_generateCI(sessk)
#unique order id
orderid=uuid.uuid4()
#make a purchase - return a transactionid
referanceid=sage_process_transaction(sessk,cardid,orderid)
neworderid=uuid.uuid4()
#make a repeat purchase - use a previosly succesfull transaction
amount=10.0
sage_process_repeat_transaction(referanceid,neworderid,amount)

'''


'''
lastupdatetime: str = '2017-01-14 15:57:11'  # last update timestamp
    o = requests.get(urlstart + '/orders.json?updated_at_min=' + lastupdatetime + '&fields=id',
                     auth=(keyp, passp))  # get the latest orders ID's
    dicto: dict = ast.literal_eval(o.text)  # convert text to dictionary
    print("call made to shopify")
    for val in dicto['orders']:  # loop the orders dictionary that contain just order ID's
        k: dict = val  # convert the string to a dictionary
        j: int = k.get('id', 0)  # get the value of the ID
        print("order stuff " + str(j))

    lo="{ \"order\": { \"email\": \"foo@example.com\", \"fulfillment_status\": \"fulfilled\", \"send_receipt\": true, \"send_fulfillment_receipt\": true, \"line_items\": [ { \"variant_id\": 49135009492, \"quantity\": 1 } ] } }"
    op = "{'order':{'line_items':[{'variant_id':49135009492,'quantity':1}],'customer':{'id':6719939092},'financial_status':'pending'}}"
    kk = { 'order': { 'email': 'cluderayd@gmail.com', 'fulfillment_status': 'fulfilled', 'line_items': [ { 'variant_id': 49135009492, 'quantity': 1 } ] } }

    fp={ 'order': { 'line_items': [ { 'variant_id': 49135009492, 'quantity': 1 } ] } }

    fullstring=urlstart + "/orders.json"

    l = requests.post(url=fullstring,json=kk,
                     auth=(keyp, passp))
'''