import requests
import responce_code
import json
import com_msg
import dac_code
import customer_functions
import hashlib
import ast

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
def update_customer_in_db(shop_first_name,shop_last_name,postcode,addressline1,addressline2,addresstown,addresscity,addressCountry,shop_id,shop_email):
    sqlcode: str = "UPDATE fred.Customers SET title = '', fname = '" + str(shop_first_name) + "', sname = '" + str(shop_last_name) + "', postcode = '" + str(postcode) + "', localshop = '1', shippingAddressLine1 = '" + str(addressline1) + "', shippingAddressLine2 = '" + str(addressline2) + "', shippingTown = '" + str(addresstown) + "', shippingCity = '" + str(addresscity) + "', shippingCountry = '" + str(addressCountry) + "', websiteid = '1', website_userid = '" + str(shop_id) + "' WHERE (Customers.email = '" + str(shop_email) + "')"
    print(sqlcode)
    dac_code.db_sql_write(sqlcode)

def insert_customer_in_db(shop_first_name,shop_last_name,postcode,addressline1,addressline2,addresstown,addresscity,addressCountry,shop_id,shop_email):
    sqlcode: str = "INSERT INTO fred.Customers(title, fname, sname, postcode, localshop, amazon_id, shippingAddressLine1, shippingAddressLine2, shippingTown, shippingCity, CustomerBillingDayofWeek, shippingCountry, websiteid, website_userid, email) VALUES ('','" + str(
        shop_first_name) + "','" + str(shop_last_name) + "','" + str(postcode) + "', '1','','" + str(
        addressline1) + "','" + str(addressline2) + "', '" + str(addresstown) + "','" + str(
        addresscity) + "','','" + str(addressCountry) + "','1', '" + str(shop_id) + "','" + str(shop_email) + "');"
    print(sqlcode)
    dac_code.db_sql_write(sqlcode)

def webhook_head(event):
    print("Entering shopify API code")
    if 'X-Shopify-Topic' in event['headers'].keys():
        callingfunction:str =""
        callingfunction=event['headers'].get('X-Shopify-Topic')
        print("Function called 'X-Shopify-Topic: " + str(callingfunction))
        bodytext:str=""
        bodytext=event.get('body')
        print("body - " + bodytext)

        if callingfunction=="carts/create":
            pass
        elif callingfunction == "carts/update":
            pass

        elif callingfunction == "customers/create":

            #add the customer to the database
            shop_id:str=""
            bodydata: dict = json.loads(bodytext)
            shop_id=bodydata.get('id')
            print(shop_id)

            shop_email:str=""
            shop_email=bodydata.get('email')
            print(shop_email)

            shop_accepts_marketing:str = ""
            shop_accepts_marketing = bodydata.get('accepts_marketing',"")
            print(shop_accepts_marketing)

            shop_created_at: str = ""
            shop_created_at = bodydata.get('created_at',"")
            print(shop_created_at)

            shop_updated_at: str = ""
            shop_updated_at = bodydata.get('updated_at',"")
            print(shop_updated_at)

            shop_first_name: str = ""
            shop_first_name = bodydata.get('first_name',"")
            print(shop_first_name)

            shop_last_name: str = ""
            shop_last_name = bodydata.get('last_name',"")


            shop_orders_count: str = ""
            shop_orders_count = bodydata.get('orders_count',"")


            shop_state: str = ""
            shop_state = bodydata.get('state',"")


            shop_total_spent: str = ""
            shop_total_spent = bodydata.get('total_spent',"")


            shop_last_order_id: str = ""
            shop_last_order_id = bodydata.get('last_order_id',"")


            shop_note: str = ""
            shop_note = bodydata.get('note',"")


            shop_verified_email: str = ""
            shop_verified_email = bodydata.get('verified_email',"")


            shop_multipass_identifier: str = ""
            shop_multipass_identifier = bodydata.get('multipass_identifier',"")


            shop_tax_exempt: str = ""
            shop_tax_exempt = bodydata.get('tax_exempt',"")


            shop_phone: str = ""
            shop_phone = bodydata.get('phone',"")


            shop_tags: str = ""
            shop_tags = bodydata.get('tags',"")


            shop_last_order_name: str = ""
            shop_last_order_name = bodydata.get('last_order_name',"")


            shop_addresses: str = ""
            shop_addresses = bodydata.get('addresses',"")
            print("Address body: " + shop_addresses)
            addressline1:str=""
            addressline2: str = ""
            addresstown: str = ""
            addresscity:str=""
            postcode: str = ""
            addressCountry:str=""

            #loop the address
            for address in shop_addresses:
                address_data: dict = json.loads(address)
                print(address_data)

            if customer_functions.check_if_customer_exists_email(shop_email)==False:
                insert_customer_in_db(shop_first_name=shop_first_name,shop_last_name=shop_last_name,postcode=postcode,addressline1=addressline1,addressline2=addressline2,addresstown=addresstown,addresscity=addresscity,addressCountry=addressCountry,shop_id=shop_id,shop_email=shop_email)
                print("creating new customer")
                #sqlcode:str="INSERT INTO fred.Customers(title, fname, sname, postcode, localshop, amazon_id, shippingAddressLine1, shippingAddressLine2, shippingTown, shippingCity, CustomerBillingDayofWeek, shippingCountry, websiteid, website_userid,email) VALUES " \
                #            "('','" + str(shop_first_name) + "','" + str(shop_last_name) + "','" + str(postcode) + "', '1','','" + str(addressline1) + "','" + str(addressline2) + "', '" + str(addresstown) + "','" + str(addresscity) + "','','" + str(addressCountry) + "','1', '" + str(shop_id) + "','" + shop_email + "');"
                #print(sqlcode)
                #dac_code.db_sql_write(sqlcode)
            else:
                update_customer_in_db(shop_first_name=shop_first_name,shop_last_name=shop_last_name,postcode=postcode,addressline1=addressline1,addressline2=addressline2,addresstown=addresstown,addresscity=addresscity,addressCountry=addressCountry,shop_id=shop_id,shop_email=shop_email)
                print("updating existing customer")
        elif callingfunction == "customers/update":
            # update customer in database
            shop_id: str = ""
            bodydata: dict = json.loads(bodytext)
            shop_id = bodydata.get('id')
            print(shop_id)

            shop_email: str = ""
            shop_email = bodydata.get('email')
            print(shop_email)

            shop_accepts_marketing: str = ""
            shop_accepts_marketing = bodydata.get('accepts_marketing', "")
            print(shop_accepts_marketing)

            shop_created_at: str = ""
            shop_created_at = bodydata.get('created_at', "")
            print(shop_created_at)

            shop_updated_at: str = ""
            shop_updated_at = bodydata.get('updated_at', "")
            print(shop_updated_at)

            shop_first_name: str = ""
            shop_first_name = bodydata.get('first_name', "")
            print(shop_first_name)

            shop_last_name: str = ""
            shop_last_name = bodydata.get('last_name', "")

            shop_orders_count: str = ""
            shop_orders_count = bodydata.get('orders_count', "")

            shop_state: str = ""
            shop_state = bodydata.get('state', "")

            shop_total_spent: str = ""
            shop_total_spent = bodydata.get('total_spent', "")

            shop_last_order_id: str = ""
            shop_last_order_id = bodydata.get('last_order_id', "")

            shop_note: str = ""
            shop_note = bodydata.get('note', "")

            shop_verified_email: str = ""
            shop_verified_email = bodydata.get('verified_email', "")

            shop_multipass_identifier: str = ""
            shop_multipass_identifier = bodydata.get('multipass_identifier', "")

            shop_tax_exempt: str = ""
            shop_tax_exempt = bodydata.get('tax_exempt', "")

            shop_phone: str = ""
            shop_phone = bodydata.get('phone', "")

            shop_tags: str = ""
            shop_tags = bodydata.get('tags', "")

            shop_last_order_name: str = ""
            shop_last_order_name = bodydata.get('last_order_name', "")

            shop_addresses: str = ""
            shop_addresses = bodydata.get('addresses', "")
            print("Address body: " + str(shop_addresses))
            addressline1: str = ""
            addressline2: str = ""
            addresstown: str = ""
            addresscity: str = ""
            postcode: str = ""
            addressCountry: str = ""

            # loop the address
            address_str:str=str(shop_addresses)

            result = ast.literal_eval(address_str)

            print("result len" + str(len(result)))

            for address in result:
                lp = json.dumps(address)
                string_withDBQuotes=lp.replace("'","\"")
                address_data: dict = json.loads(str(string_withDBQuotes))
                addressID=str(address_data.get('id'))
                customerID =str(address_data.get('customer_id'))
                firstname = str(address_data.get('first_name'))
                lastname =str(address_data.get('last_name'))
                company = str(address_data.get('company'))
                address1 = str(address_data.get('address1'))
                address2 = str(address_data.get('address2'))
                city = str(address_data.get('city'))
                province = str(address_data.get('province'))

                country=str(address_data.get('country'))
                zip = str(address_data.get('zip'))
                phone = str(address_data.get('phone'))
                country = str(address_data.get('country'))
                name = str(address_data.get('name'))
                country_code = str(address_data.get('country_code'))
                country_name = str(address_data.get('country_name'))
                default = str(address_data.get('default'))



            update_customer_in_db(shop_first_name=shop_first_name, shop_last_name=shop_last_name, postcode=postcode,
                                  addressline1=addressline1, addressline2=addressline2, addresstown=addresstown,
                                  addresscity=addresscity, addressCountry=addressCountry, shop_id=shop_id,
                                  shop_email=shop_email)
            print("updating existing customer")

        elif callingfunction == "":
            pass
        elif callingfunction == "":
            pass
        elif callingfunction == "orders/updated":
            pass
        elif callingfunction == "orders/cancelled":
            pass

        com_msg.make_mqtt_call(topic=str(callingfunction), payload=event.get('body'))
        return "bee"





