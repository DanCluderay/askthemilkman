import requests
import responce_code
import json
import com_msg
import dac_code
import customer_functions
import hashlib
import ast
from class_obj import AnOrder


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


def update_customer_address(firstname,lastname,shop_id, BillingType,CustomerID,AddressLine1,AddressLine2,AddressLine3,AddressTown,AddressCity,AddressPostcode,contact_phone,AddressCountry,Contact_name,Company_name,Default,shopify_address_id,AddressHash):
    sqlcode:str="UPDATE fred.Customer_Addresses SET BillingType = '" + str(BillingType) + "', CustomerID = '" + str(CustomerID) + "', AddressLine1 = '" + str(AddressLine1) + "', AddressLine2 = '" + str(AddressLine2) + "', AddressLine3 = '" + str(AddressLine3) + "', AddressTown = '" + str(AddressTown) + "', AddressCity = '" + str(AddressCity) + "', AddressPostcode = '" + str(AddressPostcode) + "', contact_phone = '" + str(contact_phone) + "', AddressCountry = '" + str(AddressCountry) + "', Contact_name = '" + str(Contact_name) + "', Company_name = '" + str(Company_name) + "', `Default_address` = '" + str(Default) + "', shopify_address_id = '" + str(shopify_address_id) + "', AddressHash = '" + str(AddressHash) + "' WHERE shopify_address_id = '" + str(shopify_address_id)  +"'"
    print(sqlcode)
    dac_code.db_sql_write(sqlcode)

def insert_customer_address(firstname,lastname,shop_id,BillingType,CustomerID,AddressLine1,AddressLine2,AddressLine3,AddressTown,AddressCity,AddressPostcode,contact_phone,AddressCountry,Contact_name,Company_name,Default,shopify_address_id,AddressHash):
    sqlcode:str="INSERT INTO fred.Customer_Addresses(BillingType, CustomerID, AddressLine1, AddressLine2, AddressLine3, AddressTown, AddressCity, AddressPostcode, contact_phone, AddressCountry, Contact_name, Company_name, `Default_address`, shopify_address_id, AddressHash) VALUES ('" + BillingType + "','" + CustomerID + "','" + AddressLine1 + "','" + AddressLine2 + "','" + AddressLine3 + "','" + AddressTown + "','" + AddressCity + "','" + AddressPostcode + "','" + contact_phone + "','" + AddressCountry + "','" + Contact_name + "','" + Company_name + "','" + Default + "','" + shopify_address_id + "','" + AddressHash + "');"
    print(sqlcode)
    dac_code.db_sql_write(sqlcode)

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

        elif callingfunction == "customers/update" or callingfunction == "customers/create":
            proccess_customer_updated(bodytext=bodytext)

        elif callingfunction == "orders/paid":
            #pull the order into the system
            pass
        elif callingfunction == "":
            pass
        elif callingfunction == "orders/updated":
            proccess_order_updated(bodytext=bodytext)
        elif callingfunction == "orders/cancelled":
            pass

        com_msg.make_mqtt_call(topic=str(callingfunction), payload=event.get('body'))
        return "bee"

def proccess_customer_updated(bodytext):
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
    address_str: str = str(shop_addresses)

    result = ast.literal_eval(address_str)

    print("result len" + str(len(result)))

    for address in result:
        lp = json.dumps(address)
        string_withDBQuotes = lp.replace("'", "\"")
        address_data: dict = json.loads(str(string_withDBQuotes))
        addressID = str(address_data.get('id'))
        customerID = str(address_data.get('customer_id'))
        firstname = str(address_data.get('first_name'))
        lastname = str(address_data.get('last_name'))
        company = str(address_data.get('company'))
        address1 = str(address_data.get('address1'))
        address2 = str(address_data.get('address2'))
        city = str(address_data.get('city'))
        province = str(address_data.get('province'))
        zip = str(address_data.get('zip'))
        phone = str(address_data.get('phone'))
        country = str(address_data.get('country'))
        name = str(address_data.get('name'))
        country_code = str(address_data.get('country_code'))
        country_name = str(address_data.get('country_name'))
        default = str(address_data.get('default'))
        print("default address = " + default)
        biltype = '0'
        add3 = ''

        AddressHash = ""
        shopify_id = ""
        AddressCity = ""
        if customer_functions.check_if_customer_address_exists_shopifyID(addressID) == True:

            update_customer_address(AddressHash=AddressHash, shopify_address_id=addressID, AddressCity=AddressCity,
                                    firstname=firstname, lastname=lastname, BillingType=biltype, CustomerID=customerID,
                                    AddressLine1=address1, AddressLine2=address2, AddressLine3=add3, AddressTown=city,
                                    AddressPostcode=zip, contact_phone=phone, AddressCountry=country_name,
                                    Contact_name=name, Company_name=company, Default=default, shop_id=addressID)
        else:
            insert_customer_address(AddressHash=AddressHash, shopify_address_id=addressID, AddressCity=AddressCity,
                                    firstname=firstname, lastname=lastname, BillingType=biltype, CustomerID=customerID,
                                    AddressLine1=address1, AddressLine2=address2, AddressLine3=add3, AddressTown=city,
                                    AddressPostcode=zip, contact_phone=phone, AddressCountry=country_name,
                                    Contact_name=name, Company_name=company, Default=default, shop_id=addressID)

    update_customer_in_db(shop_first_name=shop_first_name, shop_last_name=shop_last_name, postcode=postcode,
                          addressline1=addressline1, addressline2=addressline2, addresstown=addresstown,
                          addresscity=addresscity, addressCountry=addressCountry, shop_id=shop_id,
                          shop_email=shop_email)
    print("updating existing customer")
    # update glabally
    # payload:str='{ "topic":"customer", "shop":"all" }'
    payload: str = '{"topic": "customer","scope": "all_shops","ID": {"customerid": "123"}}'
    com_msg.make_mqtt_call(topic="", payload=payload)


def proccess_order_updated(bodytext):

    # body -
    # {

    #     "id": 820982911946154500,
    #     "email": "jon@doe.ca",
    #     "closed_at": null,
    #     "created_at": "2017-09-25T12:51:55-04:00",
    #     "updated_at": "2017-09-25T12:51:55-04:00",
    #     "number": 234,
    #     "note": null,
    #     "token": "123456abcd",
    #     "gateway": null,
    #     "test": true,
    #     "total_price": "6.84",
    #     "subtotal_price": "-3.16",
    #     "total_weight": 0,
    #     "total_tax": "0.00",
    #     "taxes_included": false,
    #     "currency": "USD",
    #     "financial_status": "voided",
    #     "confirmed": false,
    #     "total_discounts": "5.00",
    #     "total_line_items_price": "1.84",
    #     "cart_token": null,
    #     "buyer_accepts_marketing": true,
    #     "name": "#9999",
    #     "referring_site": null,
    #     "landing_site": null,
    #     "cancelled_at": "2017-09-25T12:51:55-04:00",
    #     "cancel_reason": "customer",
    #     "total_price_usd": null,
    #     "checkout_token": null,
    #     "reference": null,
    #     "user_id": null,
    #     "location_id": null,
    #     "source_identifier": null,
    #     "source_url": null,
    #     "processed_at": null,
    #     "device_id": null,
    #     "phone": null,
    #     "customer_locale": "en",
    #     "app_id": null,
    #     "browser_ip": null,
    #     "landing_site_ref": null,
    #     "order_number": 1234,
    #     "discount_codes": [],
    #     "note_attributes": [],
    #     "payment_gateway_names": [
    #         "visa",
    #         "bogus"
    #     ],
    #     "processing_method": "",
    #     "checkout_id": null,
    #     "source_name": "web",
    #     "fulfillment_status": "pending",
    #     "tax_lines": [],
    #     "tags": "",
    #     "contact_email": "jon@doe.ca",
    #     "order_status_url": "https://checkout.shopify.com/21197265/orders/123456abcd/authenticate?key=abcdefg",

    ################# Order Items ######################
    #     "line_items": [
    #         {
    #             "id": 866550311766439000,
    #             "variant_id": null,
    #             "title": "Heinz Mayonnaise 395g",
    #             "quantity": 1,
    #             "price": "0.59",
    #             "grams": 438,
    #             "sku": "269465",
    #             "variant_title": null,
    #             "vendor": null,
    #             "fulfillment_service": "manual",
    #             "product_id": 11142814548,
    #             "requires_shipping": true,
    #             "taxable": true,
    #             "gift_card": false,
    #             "name": "Heinz Mayonnaise 395g",
    #             "variant_inventory_management": null,
    #             "properties": [],
    #             "product_exists": true,
    #             "fulfillable_quantity": 1,
    #             "total_discount": "0.00",
    #             "fulfillment_status": null,
    #             "tax_lines": []
    #         },
    #         {
    #             "id": 141249953214522980,
    #             "variant_id": null,
    #             "title": "Magnum Classic Ice Cream 4 x 110ml",
    #             "quantity": 1,
    #             "price": "1.25",
    #             "grams": 0,
    #             "sku": "",
    #             "variant_title": null,
    #             "vendor": null,
    #             "fulfillment_service": "manual",
    #             "product_id": 11529623636,
    #             "requires_shipping": true,
    #             "taxable": true,
    #             "gift_card": false,
    #             "name": "Magnum Classic Ice Cream 4 x 110ml",
    #             "variant_inventory_management": null,
    #             "properties": [],
    #             "product_exists": true,
    #             "fulfillable_quantity": 1,
    #             "total_discount": "5.00",
    #             "fulfillment_status": null,
    #             "tax_lines": []
    #         }
    #     ],

    ############ Multipule Shipping options ###############

    #     "shipping_lines": [
    #         {
    #             "id": 271878346596884000,
    #             "title": "Generic Shipping",
    #             "price": "10.00",
    #             "code": null,
    #             "source": "shopify",
    #             "phone": null,
    #             "requested_fulfillment_service_id": null,
    #             "delivery_category": null,
    #             "carrier_identifier": null,
    #             "discounted_price": "10.00",
    #             "tax_lines": []
    #         }
    #     ],
    #     "billing_address": {
    #         "first_name": "Bob",
    #         "address1": "123 Billing Street",
    #         "phone": "555-555-BILL",
    #         "city": "Billtown",
    #         "zip": "K2P0B0",
    #         "province": "Kentucky",
    #         "country": "United States",
    #         "last_name": "Biller",
    #         "address2": null,
    #         "company": "My Company",
    #         "latitude": null,
    #         "longitude": null,
    #         "name": "Bob Biller",
    #         "country_code": "US",
    #         "province_code": "KY"
    #     },
    #     "shipping_address": {
    #         "first_name": "Steve",
    #         "address1": "123 Shipping Street",
    #         "phone": "555-555-SHIP",
    #         "city": "Shippington",
    #         "zip": "40003",
    #         "province": "Kentucky",
    #         "country": "United States",
    #         "last_name": "Shipper",
    #         "address2": null,
    #         "company": "Shipping Company",
    #         "latitude": null,
    #         "longitude": null,
    #         "name": "Steve Shipper",
    #         "country_code": "US",
    #         "province_code": "KY"
    #     },
    #     "fulfillments": [],
    #     "refunds": [],
    #     "customer": {
    #         "id": 115310627314723950,
    #         "email": "john@test.com",
    #         "accepts_marketing": false,
    #         "created_at": null,
    #         "updated_at": null,
    #         "first_name": "John",
    #         "last_name": "Smith",
    #         "orders_count": 0,
    #         "state": "disabled",
    #         "total_spent": "0.00",
    #         "last_order_id": null,
    #         "note": null,
    #         "verified_email": true,
    #         "multipass_identifier": null,
    #         "tax_exempt": false,
    #         "phone": null,
    #         "tags": "",
    #         "last_order_name": null,
    #         "default_address": {
    #             "id": 715243470612851200,
    #             "customer_id": 115310627314723950,
    #             "first_name": null,
    #             "last_name": null,
    #             "company": null,
    #             "address1": "123 Elm St.",
    #             "address2": null,
    #             "city": "Ottawa",
    #             "province": "Ontario",
    #             "country": "Canada",
    #             "zip": "K2H7A8",
    #             "phone": "123-123-1234",
    #             "name": "",
    #             "province_code": "ON",
    #             "country_code": "CA",
    #             "country_name": "Canada",
    #             "default": false
    #         }
    #     }
    # }
    #
    # "addresses": [
    #     {
    #         "id": 6844291348,
    #         "customer_id": 6719939092,
    #         "first_name": "Nic",
    #         "last_name": "cluderay",
    #         "company": "NA",
    #         "address1": "80 long lane",
    #         "address2": "carlton in lindrick",
    #         "city": "worksop",
    #         "province": "Notts",
    #         "country": "United Kingdom",
    #         "zip": "s819ar",
    #         "phone": "07881621603",
    #         "name": "Nic cluderay",
    #         "province_code": null,
    #         "country_code": "GB",
    #         "country_name": "United Kingdom",
    #         "default": true
    #     },
    #     {
    #         "id": 6924203668,
    #         "customer_id": 6719939092,
    #         "first_name": "Dan",
    #         "last_name": "Cluderay",
    #         "company": null,
    #         "address1": "approved group",
    #         "address2": "parkway close",
    #         "city": "sheffield",
    #         "province": null,
    #         "country": "United Kingdom",
    #         "zip": "S94WJ",
    #         "phone": null,
    #         "name": "Dan Cluderay",
    #         "province_code": null,
    #         "country_code": "GB",
    #         "country_name": "United Kingdom",
    #         "default": false
    #     }
    # ],
    # "default_address": {
    #     "id": 6844291348,
    #     "customer_id": 6719939092,
    #     "first_name": "Nic",
    #     "last_name": "cluderay",
    #     "company": "NA",
    #     "address1": "80 long lane",
    #     "address2": "carlton in lindrick",
    #     "city": "worksop",
    #     "province": "Notts",
    #     "country": "United Kingdom",
    #     "zip": "s819ar",
    #     "phone": "07881621603",
    #     "name": "Nic cluderay",
    #     "province_code": null,
    #     "country_code": "GB",
    #     "country_name": "United Kingdom",
    #     "default": true
    # }





    return bodytext


