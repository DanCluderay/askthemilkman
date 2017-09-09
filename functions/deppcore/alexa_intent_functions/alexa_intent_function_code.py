from alexa_responce import responce_code
from dac import dac_code

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
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
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
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
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
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
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
    dac_code(speech_output)
    print(speech_output)

    reprompt_text = "Did you get that?"
    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

