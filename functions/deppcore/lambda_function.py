#!/usr/bin/python
# Filename: mymodule.py
from __future__ import print_function
from session_vars import Singleton
import json
import com_msg
import dac_code
import customer_functions as customer_functions
import responce_code
import alexa_intent_function_code  as aifc
import local_shopify_code as l_shopify
import customer_functions as cust
import order_code
import pos_core

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
    elif intent_name=="WhatsMyOrderNumber":
        print('Enter WhatsMyOrderNumber code to return Your orderID...')
        return aifc.whatsMyOrderNumber(intent, session)
    elif intent_name == "WhatsMyCustomerNumber":
        print('Enter WhatsMyCustomerNumber code to return Your customer id...')
        return aifc.get_customerNumber(intent, session)

    elif intent_name=="connectalexa":
        print('running connectalexa...')
        return aifc.configer_to_account(intent, session)
    elif intent_name=="doyoudelivertomyaddress":
        #doyoudelivertomyaddress
        return aifc.do_you_deliver_to_my_address(intent,session)
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
        return order_code.add_something_to_an_order(intent, session)
    elif intent_name == "AddToAnOrder":
        # return get_welcome_response()
        print("adding somthing to an order")
        return order_code.add_something_to_an_order(intent, session)
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
        card_title, speech_output, reprompt_text, should_end_session),authenticate=False)


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using your local milkman" \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return responce_code.build_response({}, responce_code.build_speechlet_response(
        card_title, speech_output, None, should_end_session),authenticate=False)


def create_shopping_list_attributes(stuff):
    return {"shoppinglist": stuff}






# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("Hey there")
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
    id = str(session['user'].get('userId'))
    val = 'accessToken' in session['user']
    if val==True:
        #we have a token for this customer - store it
        accessT = str(session['user'].get('accessToken'))

    print('is userid in dict' + str(val))
    se = Singleton()
    se.set_amazon_userid(id)
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
    se.set_internal_userid(tempnum)
    print("This is the Single responce - amazon: " +str(se.get_amaozn_userid()))
    print("This is the Single responce - userid: " +str(se.get_internal_userid()))
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
    mev=str(event)
    mco=str(context)
    print('MAIN EVENT: ' + mev)
    print('MAIN CONTEXT: ' + mco)
    checkword="{'session':"

    fo=mev[0:10]
    print(mev)
    if 'func' in event.keys():
        print("Entering Func code")
        return on_function_call(event)
    elif 'resource' in event.keys():

        print("Entering shopify API code")
        if 'X-Shopify-Topic' in event['headers'].keys():# we have an event

            l_shopify.webhook_head(event)

    else:   #This is an alexa call
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

def on_function_call(event):
    function_name: str = ""
    function_params: str = ""
    function_name = event.get('func')
    function_params = event.get('val')
    print('in on_function_call code:')
    if function_name == 'test':
        return "here is a test"
    elif function_name == 'get_customers':
        fd= customer_functions.get_all_customers(1)

        return fd
    elif function_name == 'c':
        print('calling get_customer_order')
        fd= customer_functions.get_customer_current_order(function_params)

        return fd
    elif function_name == 'get_customer_order_items':
        print('calling get_customer_order_items')
        fd= customer_functions.get_customer_order_items(function_params)

        return fd
    elif function_name=="mqtt_call":
        com_msg.make_mqtt_call(function_params)

    elif function_name=="get_all_shops":
        return pos_core.get_all_store_locations()

    elif function_name=="add_new_store_location":
        return pos_core.add_store_location(function_params)

    elif function_name=="update_store_location":
        return pos_core.update_store_location(function_params)

    elif function_name=="get_productview_by_prodID":
        return pos_core.get_productview_by_ProductID(function_params)
    #
    elif function_name=="get_gridlocations":
        return pos_core.get_gridlocations(function_params)

    elif function_name=="add_node_to_loc_grid":
        return pos_core.add_node_to_loc_grid(function_params)
    #
    elif function_name=="edit_node_to_loc_grid":
        return pos_core.edit_node_to_loc_grid(function_params)
    elif function_name=="get_location_types":
        return pos_core.get_location_types()
    elif function_name=="get_location_Store_Zone_Layout":
        return pos_core.get_location_Store_Zone_Layout(function_params)

    elif function_name=="add_store_layout_row":
        return pos_core.add_store_layout_row()
    elif function_name=="edit_store_layout_row":
        return pos_core.edit__store_layout_row(function_params)


    else:
        return "func = " + str(function_name) + " val= " + str(function_params)

    return 1




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