import json
import ast
class AnOrder():

    def __init__(self):
        self.id = 0
        self.email: str = ""
        self.closedat = ""
        self.created_at = ""
        self.updated_at = ""
        self.number = 0
        self.note = ""
        self.token = ""
        self.gateway = ""
        self.test: bool = False
        self.total_price: float = 0.0
        self.subtotal_price: float = 0.0
        self.total_weight: float = 0.0
        self.total_tax: float = 0.0
        self.taxes_included: bool = False
        self.currency: str = "GPB"
        self.financial_status: str = ""
        self.confirmed: bool = False
        self.total_discounts: float = 0.0
        self.total_line_items_price: float = 0.0
        self.cart_token: str = ""
        self.buyer_accepts_marketing: bool = False
        self.name: str = ""
        self.referring_site: str = ""
        self.landing_site: str = ""
        self.cancelled_at: str = ""
        self.cancel_reason: str = ""
        self.total_price_usd: str = ""
        self.checkout_token: str = ""
        self.reference: str = ""
        self.user_id: str = ""
        self.location_id: str = ""
        self.source_identifier: str = ""
        self.source_url: str = ""
        self.processed_at: str = ""
        self.device_id: str = ""
        self.phone: str = ""
        self.customer_locale: str = ""
        self.app_id: str = ""
        self.browser_ip: str = ""
        self.landing_site_ref: str = ""
        self.order_number: int = 0

        #     "discount_codes": [],


        #     "note_attributes": [],

        #     "payment_gateway_names": [
        #         "visa",
        #         "bogus"
        #     ],
        self.processing_method: str = ""
        self.checkout_id: str = ""
        self.source_name: str = "web"
        self.fulfillment_status: str = ""

        #     "tax_lines": [],
        self.tags: str = ""
        self.contact_email: str = ""
        self.order_status_url: str = ""

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
        #

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


class CustomerDetails():

    def __init__(self, test: bool = False):
        if test == True:
            self.shopifyCustomerID: int = 1234
            self.email1: str = "dan@approvedfood.co.uk"
            self.accepts_marketing: bool = False
            self.created_at: str = "2017-10-10 00:00:00"
            self.updated_at: str = "2017-10-10 00:00:00"
            self.first_name: str = "dab"
            self.last_name: str = "cluderay"
            self.orders_count: int = 12
            self.state: str = "disabled"
            self.total_spent: float = 123.49
            self.last_order_id: int = 1231312
            self.note: str = "Hey i like your biscuits"
            self.verified_email: bool = True
            self.multipass_identifier: str = "None"
            self.tax_exempt: bool = "False"
            self.phone: str = "01909 732798"
            self.tags: str = "nothing, something"
            self.last_order_name: str = "123412342134"
            self.zip: str = "S819ar"
            self.iCustomerAddress: CustomerAddress = []
            self.localshop: int = 12
            self.amazonid: str = "1231231231231231231231"
            self.customerBillingDayOfWeek: str = "Monday"
            self.websiteID: int = 1
        else:
            self.shopifyCustomerID: int = 0
            self.email1: str = ""
            self.accepts_marketing: bool = False
            self.created_at: str = ""
            self.updated_at: str = ""
            self.first_name: str = ""
            self.last_name: str = ""
            self.orders_count: int = 0
            self.state: str = ""
            self.total_spent: float = 0.0
            self.last_order_id: int = 0
            self.note: str = ""
            self.verified_email: bool = True
            self.multipass_identifier: str = ""
            self.tax_exempt: bool = ""
            self.phone: str = ""
            self.tags: str = ""
            self.last_order_name: str = ""
            self.zip: str = ""
            self.iCustomerAddress: CustomerAddress = []
            self.localshop: int = 0
            self.amazonid: str = ""
            self.customerBillingDayOfWeek: str = ""
            self.websiteID: int = 1

    def __getitem__(self, index):
        return self

    def convert_json_bodytext_to_Customer(self,bodytext):

        bodydata: dict = json.loads(bodytext)
        self.shopifyCustomerID = bodydata.get('id')
        print(self.shopifyCustomerID)

        self.email1 = bodydata.get('email')
        print(self.email1)

        self.accepts_marketing = bodydata.get('accepts_marketing', "")
        print(self.accepts_marketing )

        self.created_at = bodydata.get('created_at', "")
        print(self.created_at)

        self.updated_at = bodydata.get('updated_at', "")
        print(self.updated_at)

        self.first_name = bodydata.get('first_name', "")
        print(self.first_name)

        self.last_name = bodydata.get('last_name', "")

        self.orders_count = bodydata.get('orders_count', 0)

        self.state = bodydata.get('state', "")

        self.total_spent = bodydata.get('total_spent', "")

        self.last_order_id = bodydata.get('last_order_id', "")

        self.note = bodydata.get('note', "")

        self.verified_email = bodydata.get('verified_email', "")

        self.multipass_identifier = bodydata.get('multipass_identifier', "")

        self.tax_exempt = bodydata.get('tax_exempt', "")

        self.phone = bodydata.get('phone', "")

        self.tags = bodydata.get('tags', "")

        self.last_order_name = bodydata.get('zip', "")

        self.zip = bodydata.get('last_order_name', "")
        self.websiteID = 1
        shop_addresses: str = ""
        shop_addresses = bodydata.get('addresses', "")
        print("Address body: " + str(shop_addresses))
        c=CustomerAddress()
        self.iCustomerAddress=c.convert_json_bodytext_to_CustomerAddress(shop_addresses)

        return self

class CustomerAddress():

    def __init__(self):

        self.id:int=0
        self.customer_id:int=0
        self.first_name:str=""
        self.last_name: str = ""
        self.company: str = ""

        self.address1: str = ""
        self.address2: str = ""
        self.town:str=""
        self.city: str = ""

        self.province: str = ""
        self.zip: str = ""
        self.phone: str = ""
        self.country: str = ""

        self.name: str = ""
        self.country_code: str = ""
        self.country_name: str = ""
        self.default: str = ""
        self.Billtype:int=0
        self.address3:str=""

    def __getitem__(self, index):
        return self

    def convert_json_bodytext_to_CustomerAddress(self,bodytext):
        result = ast.literal_eval(str(bodytext))

        print("result len" + str(len(result)))
        ret_list=[]
        for address in result:
            lp = json.dumps(address)
            string_withDBQuotes = lp.replace("'", "\"")
            address_data: dict = json.loads(str(string_withDBQuotes))
            new_address:CustomerAddress=CustomerAddress()
            new_address.id = str(address_data.get('id'))
            new_address.customer_id = str(address_data.get('customer_id'))
            new_address.first_name = str(address_data.get('first_name'))
            new_address.last_name = str(address_data.get('last_name'))
            new_address.company = str(address_data.get('company'))
            new_address.address1 = str(address_data.get('address1'))
            new_address.address2 = str(address_data.get('address2'))
            new_address.city = str(address_data.get('city'))
            new_address.province = str(address_data.get('province'))
            new_address.zip = str(address_data.get('zip'))
            new_address.phone = str(address_data.get('phone'))
            new_address.country = str(address_data.get('country'))
            new_address.name = str(address_data.get('name'))
            new_address.country_code = str(address_data.get('country_code'))
            new_address.country_name = str(address_data.get('country_name'))
            new_address.default = str(address_data.get('default'))
            print("default address = " + new_address.default)
            biltype = '0'
            add3 = ''
            #if len(ret_list)==0:
            #    ret_list.insert(0,new_address)
            #else:
            ret_list.insert(len(ret_list), new_address)
        return ret_list

#g=CustomerDetails(test=True)

#b='{ "id": 6719939092, "email": "cluderayd@gmail.com", "accepts_marketing": false, "created_at": "2017-07-02T17:39:01+01:00", "updated_at": "2017-09-27T15:52:55+01:00", "first_name": "Nic", "last_name": "cluderay", "orders_count": 13, "state": "disabled", "total_spent": "1.57", "last_order_id": 5988531732, "note": null, "verified_email": true, "multipass_identifier": null, "tax_exempt": false, "phone": null, "tags": "", "last_order_name": "#1016", "addresses": [ { "id": 6844291348, "customer_id": 6719939092, "first_name": "Nic", "last_name": "cluderay", "company": "NA", "address1": "80 long lane", "address2": "carlton in lindrick", "city": "worksop WILLY", "province": "Notts", "country": "United Kingdom", "zip": "s819ar", "phone": "07881621603", "name": "Nic cluderay", "province_code": null, "country_code": "GB", "country_name": "United Kingdom", "default": false }, { "id": 6924203668, "customer_id": 6719939092, "first_name": "Dan", "last_name": "Cluderay", "company": "", "address1": "approved group", "address2": "parkway close todger", "city": "sheffield", "province": "", "country": "United Kingdom", "zip": "S94WJ", "phone": "", "name": "Dan Cluderay", "province_code": null, "country_code": "GB", "country_name": "United Kingdom", "default": true } ], "default_address": { "id": 6924203668, "customer_id": 6719939092, "first_name": "Dan", "last_name": "Cluderay", "company": "", "address1": "approved group", "address2": "parkway close todger", "city": "sheffield", "province": "", "country": "United Kingdom", "zip": "S94WJ", "phone": "", "name": "Dan Cluderay", "province_code": null, "country_code": "GB", "country_name": "United Kingdom", "default": true } }'
#h=g.convert_json_bodytext_to_Customer(b)
# g.iCustomerAddress=[CustomerAddress()]
# m:CustomerAddress=CustomerAddress()
# n:CustomerAddress=CustomerAddress()
# o:CustomerAddress=CustomerAddress()
# g.iCustomerAddress.insert(len(g.iCustomerAddress),m)
# g.iCustomerAddress.insert(len(g.iCustomerAddress),n)
# g.iCustomerAddress.insert(len(g.iCustomerAddress),o)
# g.iCustomerAddress[0].last_name="cluderay"
# print(g.iCustomerAddress[0].last_name)
#pass




