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

def create_new_product(para):

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
    imagepath=str(ob['imagepath'])

    shop_url = "https://%s:%s@dans-daily-deals.myshopify.com/admin" % (keyp, passp)
    shopify.ShopifyResource.set_site(shop_url)
    new_product = Product()
    pid = 0
    new_product.vendor = vendor
    new_product.title = title
    new_product.product_type = product_type
    new_product.body_html = body_html

    image1 = shopify.Image()
    image1.src = imagepath
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
