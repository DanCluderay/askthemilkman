import responce_code
import dac_code
import customer_functions

from session_vars import Singleton


def get_customerNumber(intent, session):
    se = Singleton()

    # find the customer ID from amazonID
    customernubmer = customer_functions.get_internal_userid(intent, session)
    speech_output = "Your order customer number is " + str(customernubmer)
    print(speech_output)
    session_attributes = {}
    card_title = "DEBUG - This is your customer id"
    #
    reprompt_text = "Did you get that?"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session), authenticate=False)


def whatsMyOrderNumber(intent, session):
    print("whatsMyOrderNumber... creating singleton class" )
    se = Singleton()

    #find the customer ID from amazonID
    amid=se.get_amaozn_userid()
    print("whatsMyOrderNumber... getting amzonid" + str(amid))
    print("whatsMyOrderNumber... gettign customer id")
    customerid:int=customer_functions.check_customer_by_amazonid(amid)
    print("whatsMyOrderNumber... customer ID is " + str(customerid))
    orderid:int=customer_functions.get_customer_current_order_number_from_id(customerid)
    print("whatsMyOrderNumber... order ID is " + str(orderid))
    if orderid==0:
        #create a new order
        print("whatsMyOrderNumber... creating new order")
        yourOrderNum=customer_functions.create_new_order(customerid)
    else:
        yourOrderNum = orderid


    speech_output="Your order number is " + str(yourOrderNum)
    print(speech_output)
    session_attributes = {}
    card_title = "DEBUG - This is your orderid"
    #
    reprompt_text = ""
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session), authenticate=False)


def do_you_deliver_to_my_address(intent, session):
    se = Singleton()

    custdict: dict = {}
    sessionid=''
    #get the customer data
    custdict=customer_functions.get_customer_details(se.get_internal_userid())

    #if the customer has a shop assigned then we just answer -YES! we've already done the search

    #if no then we need to perform the query and set the shop covered

    dowedeliver:int=0
    speech_output:str = ""
    if dowedeliver==0 :
        #we dont deliver
        speech_output="Sorry, we don't deliver in your area yet"
        pass
    elif dowedeliver==1:
        #we deliver with a really fast service
        speech_output = "Great news, we have a 1 hour service in your area"
        pass
    elif dowedeliver==2:
        #we deliver with a 1 day service
        speech_output = "Good news, we have a same day service in your area"
        pass
    elif dowedeliver==3:
        #plus one day delivery
        speech_output = "We can deliver goods next day for your area"
        pass

    session_attributes = {}
    card_title = "Does the milkman deliver to your address"
     #
    reprompt_text = "Did you get that?"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session),authenticate=False)


def configer_to_account(intent, session):
    pass
    #reserve a word to the
    session_attributes = {}
    card_title = "Alexa connection"
    speech_output = "Your special password to enter is <break time=\"0.5s\"/>  DOG "  #
    reprompt_text = "Did you get that?"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session),authenticate=False)

def place_order_and_deliver(intent, session):
    print("place order and deliver calue " + str(intent))
    session_attributes = {}
    card_title = "Order Delivery"
    speech_output = "Yes, i can deliver your order now"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Did you get that?"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session),authenticate=False)


def how_much_is_my_order(intent, session):
    print("This is the cost " + str(intent) + " to the order")
    session_attributes = {}
    card_title = "Your Shopping list"
    speech_output = "Youve spent £10 this week"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Did you get that?"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session),authenticate=False)

def whats_on_my_shopping_list(intent, session):
    print("whats_on_my_shopping_list " + str(intent) + " to the order")
    session_attributes = {}
    card_title = "Your Shopping list"
    speech_output = "I've 10 things on your shopping list"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Did you get that?"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session),authenticate=False)


def add_item_to_order(intent, session):
    print("Ive added " + str(intent) + " to the order")

    session_attributes = {}
    card_title = "I've added milk to your order"
    speech_output = "I've added milk to your order"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Did you get that?"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session),authenticate=False)


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
    dac_code(speech_output)
    print(speech_output)

    reprompt_text = ""
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session),authenticate=False)

