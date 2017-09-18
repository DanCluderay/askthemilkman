import requests
import responce_code
import globalvars as gv


def Create_Order():
    print("order creating")
    
    #things we need to create an order
    #+ get all the items in the list
    #++ Product varient and qty

    '''
    
    orderjson = { 'order': { 'email': 'cluderayd@gmail.com', 'fulfillment_status': 'fulfilled', 'line_items': [ { 'variant_id': 49135009492, 'quantity': 1 } ] } } fullstring=gv. urlstart + "/orders.json"

    l = requests.post(url=fullstring,json =orderjson,
                      auth=(gv.keyp, gv.passp))

    print(str(l))
    session_attributes = {}
    card_title = "Order created"
    speech_output = "Great, we have created an invoice and emailed it to you. Will we take payment on Friday"

    reprompt_text = "Is there anything else?"

    should_end_session = False
    return responce_code.build_response(session_attributes, responce_code.build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
    '''






