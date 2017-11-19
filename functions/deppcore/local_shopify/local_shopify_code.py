import requests
import responce_code
import json
import com_msg
import dac_code
import customer_functions
import hashlib
import ast
from class_obj import AnOrder, CustomerDetails, CustomerAddress
import shopify
from shopify import Product

keyp: str = "461824c0a06d4be0e94851deeabc3965"
passp: str = "9bb4f551ba4888c9199b7a9509f0e872"
urlstart: str = "https://dans-daily-deals.myshopify.com/admin"
urldom:str="@dans-daily-deals.myshopify.com/admin"

def shopify_get_product():
    product = shopify.Product.find(5036662947872)

def shopify_create_new_product(para):

    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))
    vendor = str(ob['vendor'])
    title = str(ob['title'])
    product_type = str(ob['product_type'])
    body_html = str(ob['body_html'])

    barcode = str(ob['barcode'])
    compare_at_price = str(ob['compare_at_price'])
    grams = str(ob['grams'])
    inventory_quantity = str(ob['inventory_quantity'])
    price = str(ob['price'])
    sku = str(ob['sku'])
    taxable = str(ob['taxable'])
    weight = float(ob['weight'])
    weight_unit = str(ob['weight_unit'])
    inventory_management = str(ob['inventory_management'])
    tags = str(ob['tags'])

    shop_url = "https://%s:%s@dans-daily-deals.myshopify.com/admin" % (keyp, passp)
    shopify.ShopifyResource.set_site(shop_url)
    new_product = Product()
    pid = 0
    new_product.vendor = vendor
    new_product.title = title
    new_product.product_type = product_type
    new_product.body_html = body_html

    image_filename = "http://fthumb.approvedfood.co.uk/thumbs/75/1000/296/1/src_images/hersheys_creamy_milk_chocolate_with_almonds_43g.jpg"
    image1 = shopify.Image()
    image1.src = image_filename
    print(image1.src)
    new_product.images = [image1]

    success = new_product.save()  # returns false if the record is invalid

    new_product.attributes['tags'] = tags
    new_product.attributes['variants'][0].attributes['tags'] = tags
    new_product.attributes['variants'][0].attributes['barcode'] = barcode
    new_product.attributes['variants'][0].attributes['compare_at_price'] = compare_at_price
    new_product.attributes['variants'][0].attributes['grams'] = grams
    new_product.attributes['variants'][0].attributes['inventory_quantity'] = inventory_quantity
    new_product.attributes['variants'][0].attributes['price'] = price
    new_product.attributes['variants'][0].attributes['sku'] = sku
    new_product.attributes['variants'][0].attributes['taxable'] = taxable
    new_product.attributes['variants'][0].attributes['title'] = title
    new_product.attributes['variants'][0].attributes['weight'] = weight
    new_product.attributes['variants'][0].attributes['weight_unit'] = weight_unit
    new_product.attributes['variants'][0].attributes['inventory_management'] = inventory_management

    # inventory-management>shopify

    success = new_product.save()
    print(success)

    return new_product.attributes['variants'][0].id

'''
This function is called with a stock level varient ID
'''


def shopify_update_product(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    product_stock_VID: str = str(
        ob['product_stock_VID'])  # Check if its an insert or update by looking at if there is a ProductID
    # check if shopify is aware of this sku
    # get the product details from the database required to create / update shopify
    #
    # if its not in the system create it


    # if it IS in the system then update


def Create_Order():
    print("order creating")

    # things we need to create an order
    # + get all the items in the list
    # ++ Product varient and qty

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


'''Updates the customer address table'''


def update_customer_address_via_obj(ad: CustomerAddress):
    sqlcode: str = "UPDATE fred.Customer_Addresses SET BillingType = '0', CustomerID = " + str(
        ad.customer_id) + ", first_name = '" + str(ad.first_name) + "', last_name = '" + str(
        ad.last_name) + "', AddressLine1 = '" + str(ad.address1) + "', AddressLine2 = '" + str(
        ad.address2) + "', AddressLine3 = '', AddressCity = '" + str(ad.city) + "', AddressProvince = '" + str(
        ad.province) + "', AddressPostcode = '" + str(ad.zip) + "', contact_phone = '" + str(
        ad.phone) + "', AddressCountry = '" + str(ad.country) + "', Contact_name = '" + str(
        ad.name) + "', Company_name = '" + str(ad.company) + "', `Default_address` = '" + str(
        ad.default) + "', shopify_address_id = '" + str(
        ad.id) + "', AddressHash = '' WHERE shopify_address_id = '" + str(ad.id) + "'"
    print(sqlcode)
    dac_code.db_sql_write(sqlcode)


'''insterts new addresses'''


def insert_customer_address_via_obj(ad: CustomerAddress):
    sqlcode: str = "INSERT INTO fred.Customer_Addresses(BillingType, CustomerID, first_name, last_name, AddressLine1, AddressLine2, AddressLine3, AddressCity, AddressProvince, AddressPostcode, contact_phone, AddressCountry, Contact_name, Company_name, `Default_address`, shopify_address_id, AddressHash) VALUES ('0'," + ad.customer_id + ",'" + ad.first_name + "','" + ad.last_name + "','" + ad.address1 + "','" + ad.address2 + "','','" + ad.city + "','" + ad.province + "','" + ad.zip + "','" + ad.phone + "','" + ad.country + "','" + ad.name + "','" + ad.company + "','" + ad.default + "','" + ad.id + "','');"
    print(sqlcode)
    dac_code.db_sql_write(sqlcode)


def update_customer_in_db_via_obj(ob: CustomerDetails):
    sqlcode: str = "UPDATE fred.Customers SET title = '', fname = '" + str(ob.first_name) + "', sname = '" + str(
        ob.last_name) + "', websiteid='" + str(ob.websiteID) + "', email='" + str(ob.email1) + "', hometel='" + str(
        ob.phone) + "', accepts_marketing='" + str(
        convert_string_to_int(ob.accepts_marketing)) + "', web_created_at='" + str(
        ob.created_at) + "', web_updated_at='" + str(ob.updated_at) + "', web_State='" + str(
        ob.state) + "', web_last_order_id='" + str(convert_int_for_sql(ob.last_order_id)) + "', web_note='" + str(
        ob.note) + "', verified_email=" + str(
        convert_string_to_int(ob.verified_email)) + ", multipass_identifier='" + str(
        ob.multipass_identifier) + "', tax_exempt=" + str(convert_string_to_int(ob.tax_exempt)) + ", web_tags='" + str(
        ob.tags) + "', web_Last_order_ID_str='" + str(
        ob.last_order_name) + "' WHERE (Customers.shopify_userid = " + str(ob.shopifyCustomerID) + ")"
    print(sqlcode)
    dac_code.db_sql_write(sqlcode)


def insert_customer_in_db_via_obj(ob: CustomerDetails):
    print("updating address via object")
    sqlcode: str = "INSERT INTO fred.Customers(fname, sname, websiteid, shopify_userid, email, hometel, accepts_marketing, web_created_at, web_updated_at, web_LifetimeOrderCount, web_LifeTimeOrderSpend, web_State, web_last_order_id, web_note, verified_email, multipass_identifier, tax_exempt, web_tags, web_Last_order_ID_str) VALUES ('" + str(
        ob.first_name) + "','" + str(ob.last_name) + "','" + str(ob.websiteID) + "','" + str(
        ob.shopifyCustomerID) + "','" + str(ob.email1) + "','" + str(ob.phone) + "','" + str(
        convert_string_to_int(ob.accepts_marketing)) + "','" + str(ob.created_at) + "','" + str(
        ob.updated_at) + "','" + str(ob.orders_count) + "','" + str(ob.total_spent) + "','" + str(
        ob.state) + "'," + str(convert_int_for_sql(ob.last_order_id)) + ",'" + str(ob.note) + "','" + str(
        convert_string_to_int(ob.verified_email)) + "','" + "', '" + str(
        convert_string_to_int(ob.tax_exempt)) + "','" + str(ob.tags) + "','" + str(ob.last_order_name) + "');"
    print(sqlcode)
    dac_code.db_sql_write(sqlcode)


def convert_string_to_int(thestring: str):
    ret_val: int = 0
    if thestring == "True":
        ret_val = 1
    else:
        ret_val = 0

    return ret_val


def convert_int_for_sql(theint: int):
    ret_val: int = 0
    if theint == None:
        ret_val = 0
    else:
        ret_val = theint
    return ret_val


def webhook_head(event):
    print("Entering shopify API code")
    if 'X-Shopify-Topic' in event['headers'].keys():
        callingfunction: str = ""
        callingfunction = event['headers'].get('X-Shopify-Topic')
        print("Function called 'X-Shopify-Topic: " + str(callingfunction))
        bodytext: str = ""
        bodytext = event.get('body')
        print("body - " + bodytext)

        if callingfunction == "carts/create":
            pass
        elif callingfunction == "carts/update":
            pass

        elif callingfunction == "customers/update" or callingfunction == "customers/create":
            customer_object: CustomerDetails = CustomerDetails.convert_json_bodytext_to_Customer(self=CustomerDetails,
                                                                                                 bodytext=bodytext)
            if customer_functions.check_if_customer_exists_shopify_customerid(customer_object.shopifyCustomerID):
                print("calling object customer update")
                print("email! " + str(customer_object.email1))
                update_customer_in_db_via_obj(customer_object)
            else:
                print("calling object customer Insert")
                print("email! " + str(customer_object.email1))
                insert_customer_in_db_via_obj(customer_object)
            print("Address Len " + str(len(CustomerDetails.iCustomerAddress)))
            x: int = 0
            for ob in CustomerDetails.iCustomerAddress:
                print(str(CustomerDetails.iCustomerAddress[x].first_name))
                print(str(ob.first_name))
                if customer_functions.check_if_customer_address_exists_shopifyID(
                        CustomerDetails.iCustomerAddress[x].id) == True:
                    update_customer_address_via_obj(CustomerDetails.iCustomerAddress[x])
                else:
                    insert_customer_address_via_obj(CustomerDetails.iCustomerAddress[x])
                print("x value " + str(x))
                x = x + 1

        elif callingfunction == "orders/paid":
            # pull the order into the system
            pass
        elif callingfunction == "":
            pass
        elif callingfunction == "orders/updated":
            proccess_order_updated(bodytext=bodytext)
        elif callingfunction == "orders/cancelled":
            pass

        com_msg.make_mqtt_call(topic=str(callingfunction), payload=event.get('body'))
        return "bee"


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

#shopify_create_new_product()

