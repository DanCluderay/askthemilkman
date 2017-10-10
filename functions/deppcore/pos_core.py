import dac_code
import com_msg
import json
import random
import shopify
import requests

keyp:str ="461824c0a06d4be0e94851deeabc3965"
passp:str  ="9bb4f551ba4888c9199b7a9509f0e872"
urlstart:str ="https://dans-daily-deals.myshopify.com/admin"

def get_all_store_locations():
    sqlcode = "SELECT stores.store_autoid, stores.store_name, stores.store_shortcode  FROM fred.stores stores"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result

def add_store_location(para):

    quoteless=para.replace("\'","\"")
    ob:dict=json.loads(quoteless)
    print(str(ob))
    shopname=ob['shopname']
    shopcode:str=ob['shopcode']
    sqlstring:str="INSERT INTO fred.stores(store_name, store_shortcode) VALUES ('" + shopname + "', '" + shopcode + "');"
    print(sqlstring)
    dac_code.db_sql_write(sqlstring)

    callingfunction="global/store_update"
    paypacket:str="{ 'updatetask':'store_locations'}"
    com_msg.make_mqtt_call(topic=str(callingfunction), payload=paypacket)
    pass


def update_store_location(para):

    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))
    shopname = ob['shopname']
    shopcode: str = ob['shopcode']
    shopid=ob['shopid']
    sqlstring: str = "UPDATE fred.stores SET store_name = '" + shopname + "', store_shortcode = '" + shopcode + "' WHERE store_autoid=" + shopid + ";"
    dac_code.db_sql_write(sqlstring)

    callingfunction="global/store_update"
    paypacket:str="{ 'updatetask':'store_locations'}"
    com_msg.make_mqtt_call(topic=str(callingfunction), payload=paypacket)
    pass

def get_productview_by_ProductID(productid):
    sqlstring="SELECT Product_Varient_Location_Stock_qty.*, ProductTypes.ProductTypesautoid, ProductVarient.pv_Name, stores.store_name FROM ((fred.ProductVarient ProductVarient INNER JOIN fred.Product_Varient_Location_Stock_qty Product_Varient_Location_Stock_qty ON (ProductVarient.pv_autoID = Product_Varient_Location_Stock_qty.Varient_Instance_ID)) INNER JOIN fred.ProductTypes ProductTypes ON (ProductTypes.ProductTypesautoid = ProductVarient.product_type_id)) INNER JOIN fred.stores stores ON (stores.store_autoid = Product_Varient_Location_Stock_qty.Varient_Location_ID) WHERE (ProductTypes.ProductTypesautoid = " + productid  + ")"

    result = dac_code.dbreadquery_sql(sqlstring)

    #Loop the result and fetch the stock qty for each varient
    for x in result:
        print(str(x))


        Varient_Instance_ID = x['Varient_Instance_ID']
        #go to shopify and get the stock value
        x['ForSale']=random.randint(0,96)
        x['Inbasket']=random.randint(0,24)
        x['sold']=random.randint(0,12)
        x['reserve']=random.randint(6,12)
        x['transit']=random.randint(100,200)
    return result


def get_gridlocations(gridref):
    sqlstring = "SELECT Location_Grid.LocGridID, Location_Grid.LocName, Location_Grid.LocType, Location_Grid.LocParent, Location_Grid.Updated_at, Location_Grid.Created_at FROM fred.Location_Grid Location_Grid"

    result = dac_code.dbreadquery_sql(sqlstring)
    return result

#get_productview_by_ProductID("1")

def get_all_products():
    pd=shopify.Product()
    pd = requests.get(urlstart + "/products.json?fields=variant.id,variant.inventory_quantity",auth=(keyp,passp))#id,

    print(pd)

#get_all_products()