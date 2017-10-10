import dac_code
import com_msg
import json
import ast

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

    return result
