import dac_code
import com_msg
import json
import random
import shopify
import requests
import uuid

keyp: str = "461824c0a06d4be0e94851deeabc3965"
passp: str = "9bb4f551ba4888c9199b7a9509f0e872"
urlstart: str = "https://dans-daily-deals.myshopify.com/admin"


def get_all_store_locations():
    sqlcode = "SELECT stores.store_autoid, stores.store_name, stores.store_shortcode  FROM fred.stores stores"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result


def add_store_location(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))
    shopname = ob['shopname']
    shopcode: str = ob['shopcode']
    sqlstring: str = "INSERT INTO fred.stores(store_name, store_shortcode) VALUES ('" + shopname + "', '" + shopcode + "');"
    print(sqlstring)
    dac_code.db_sql_write(sqlstring)

    callingfunction = "global/store_update"
    paypacket: str = "{ 'updatetask':'store_locations'}"
    com_msg.make_mqtt_call(topic=str(callingfunction), payload=paypacket)
    pass


def update_store_location(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))
    shopname = ob['shopname']
    shopcode: str = ob['shopcode']
    shopid = ob['shopid']
    sqlstring: str = "UPDATE fred.stores SET store_name = '" + shopname + "', store_shortcode = '" + shopcode + "' WHERE store_autoid=" + shopid + ";"
    dac_code.db_sql_write(sqlstring)

    callingfunction = "global/store_update"
    paypacket: str = "{ 'updatetask':'store_locations'}"
    com_msg.make_mqtt_call(topic=str(callingfunction), payload=paypacket)
    pass


def get_productview_by_ProductID(productid):
    sqlstring = "SELECT Product_Instance.pv_autoID, Product_Instance.productID, Product_Instance.pv_Name FROM fred.Product_Instance Product_Instance INNER JOIN fred.Products Products ON (Product_Instance.productID = Products.ProductID) WHERE (Products.ProductID = " + str(
        productid) + ")"

    result = dac_code.dbreadquery_sql(sqlstring)

    # Loop the result and fetch the stock qty for each varient
    for x in result:
        print(str(x))

        Varient_Instance_ID = x['Varient_Instance_ID']
        # go to shopify and get the stock value
        x['ForSale'] = random.randint(0, 96)
        x['Inbasket'] = random.randint(0, 24)
        x['sold'] = random.randint(0, 12)
        x['reserve'] = random.randint(6, 12)
        x['transit'] = random.randint(100, 200)
    return result


def get_gridlocations(gridref):
    sqlstring = "SELECT Location_Grid.LocGridID, Location_Grid.LocName, Location_Grid.LocType, Location_Grid.LocParent, Location_Grid.PickOrder, Location_Grid.FullName, Location_Grid.ShortName FROM fred.Location_Grid Location_Grid ORDER BY Location_Grid.PickOrder ASC"

    result = dac_code.dbreadquery_sql(sqlstring)
    return result


# get_productview_by_ProductID("1")

def get_all_products():
    pd = shopify.Product()
    pd = requests.get(urlstart + "/products.json?fields=variant.id,variant.inventory_quantity",
                      auth=(keyp, passp))  # id,

    print(pd)


def add_node_to_loc_grid(para):
    locname: str = ""
    loctype: int = 0
    locparent: int = 0
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))
    FullName = str(ob['FullName'])
    ShortName = str(ob['ShortName'])
    PickOrder = str(ob['PickOrder'])

    locname = str(ob['LocName'])
    loctype = int(ob['LocType'])
    locparent = int(ob['LocParent'])
    GU: str = uuid.uuid4()

    sqlstring: str = "INSERT INTO fred.Location_Grid(LocName, LocParent, LocType, GUID, FullName, ShortName, PickOrder) VALUES ('" + locname + "','" + str(
        locparent) + "','" + str(loctype) + "','" + str(GU) + "','" + str(FullName) + "','" + str(
        ShortName) + "','" + str(PickOrder) + "');"
    print(sqlstring)
    dac_code.db_sql_write(sqlstring)

    callingfunction = "global/locations_updated"
    paypacket: str = "{ 'updatetask':'locations_updated'}"
    com_msg.make_mqtt_call(topic=str(callingfunction), payload=paypacket)
    return get_location_gridID_fromGUID(GU)


def get_location_gridID_fromGUID(GU):
    sqlcode = "SELECT Location_Grid.LocGridID  FROM fred.Location_Grid Location_Grid WHERE (Location_Grid.GUID = '" + str(
        GU) + "')"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result


def edit_node_to_loc_grid(para):
    locname: str = ""
    loctype: int = 0
    locparent: int = 0
    locid: int = 0
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))
    locname = str(ob['LocName'])
    loctype = int(ob['LocType'])
    locparent = int(ob['LocParent'])

    FullName = str(ob['FullName'])
    ShortName = str(ob['ShortName'])
    PickOrder = str(ob['PickOrder'])

    locid = int(ob['LocGridID'])

    sqlstring: str = "UPDATE fred.Location_Grid SET LocName = '" + str(locname) + "', LocParent = '" + str(
        locparent) + "', LocType = '" + str(loctype) + "' WHERE LocGridID=" + str(locid)
    print(sqlstring)
    dac_code.db_sql_write(sqlstring)

    callingfunction = "global/locations_updated"
    paypacket: str = "{ 'updatetask':'locations_updated'}"
    com_msg.make_mqtt_call(topic=str(callingfunction), payload=paypacket)
    return get_gridlocations("")


def get_location_types():
    sqlcode = "SELECT Location_Type.LocationTypeID, Location_Type.LocationName  FROM fred.Location_Type Location_Type"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result


def get_location_Store_Zone_Layout(storeid):
    sqlcode = "SELECT storelayout.id, storelayout.BuildingID, storelayout.LocGrid_ID, storelayout.Control_Type, storelayout.Control_X, storelayout.Control_Y,Control_Size FROM fred.storelayout storelayout WHERE (storelayout.BuildingID = " + str(
        storeid) + ")"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result


def get_location_Store_Zone_Funiture():
    sqlcode = "SELECT store_control_type.store_control_type_id, store_control_type.store_control_name, store_control_type.store_control_name_desc, store_control_type.store_control_subtype FROM fred.store_control_type store_control_type"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result


def add_store_layout_row(para):
    BuildingID: int = 0
    LocGrid_ID: int = 0
    Control_Type: int = 0
    Control_Y: int = 0
    Control_X: int = 0
    Control_Z: int = 0
    Control_Size: int = 0

    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))
    BuildingID = str(ob['BuildingID'])
    LocGrid_ID = int(ob['LocGrid_ID'])
    Control_Type = int(ob['Control_Type'])
    Control_X = int(ob['Control_X'])
    Control_Y = int(ob['Control_Y'])
    Control_Z = int(ob['Control_Z'])
    Control_Size = int(ob['Control_Size'])

    sqlstring: str = "INSERT INTO fred.storelayout(BuildingID, LocGrid_ID, Control_Type, Control_Y, Control_X, Control_Z, Control_Size) VALUES (" + str(
        BuildingID) + "," + str(LocGrid_ID) + "," + str(Control_Type) + "," + str(Control_Y) + "," + str(
        Control_X) + "," + str(Control_Z) + "," + str(Control_Size) + ");"
    print(sqlstring)
    dac_code.db_sql_write(sqlstring)

    # callingfunction = "global/locations_updated"
    # paypacket: str = "{ 'updatetask':'locations_updated'}"
    # com_msg.make_mqtt_call(topic=str(callingfunction), payload=paypacket)
    return get_location_Store_Zone_Layout(LocGrid_ID)


def edit__store_layout_row(para):
    BuildingID: int = 0
    LocGrid_ID: int = 0
    Control_Type: int = 0
    Control_Y: int = 0
    Control_X: int = 0
    Control_Z: int = 0

    id: int = 0  # Where clause

    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))
    BuildingID = str(ob['BuildingID'])
    LocGrid_ID = int(ob['LocGrid_ID'])
    Control_Type = int(ob['Control_Type'])
    Control_X = int(ob['Control_X'])
    Control_Y = int(ob['Control_Y'])
    Control_Z = int(ob['Control_Z'])
    Control_Size = int(ob['Control_Size'])
    id = int(ob['id'])

    sqlstring: str = "UPDATE fred.storelayout SET BuildingID =" + str(BuildingID) + ", LocGrid_ID =" + str(
        LocGrid_ID) + ", Control_Type =" + str(Control_Type) + ", Control_Y =" + str(Control_Y) + ", Control_X =" + str(
        Control_X) + ", Control_Z =" + str(Control_Z) + ", Control_Size=" + str(Control_Size) + " WHERE id=" + str(id)
    print("Updating Store layout " + sqlstring)

    dac_code.db_sql_write(sqlstring)

    # callingfunction = "global/locations_updated"
    # paypacket: str = "{ 'updatetask':'locations_updated'}"
    # com_msg.make_mqtt_call(topic=str(callingfunction), payload=paypacket)
    return get_location_Store_Zone_Layout(LocGrid_ID)


def get_product_use_cases():
    sqlcode = "SELECT Product_Use_Case.id, Product_Use_Case.Statement, Product_Use_Case.ParentID, Product_Use_Case.TAG FROM fred.Product_Use_Case Product_Use_Case"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result


def add_product_use_cases(para):
    Statement: str = 0
    ParentID: int = 0
    TAG: str = ""

    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))

    Statement = str(ob['Statement'])
    ParentID = int(ob['ParentID'])
    TAG = str(ob['TAG'])

    sqlstring: str = "INSERT INTO fred.Product_Use_Case(Statement, ParentID, TAG) VALUES ('" + str(
        Statement) + "'," + str(ParentID) + ",'" + str(TAG) + "');"
    print("Updating Store layout " + sqlstring)

    dac_code.db_sql_write(sqlstring)


def edit_product_use_cases(para):
    id: int = 0
    Statement: str = 0
    ParentID: int = 0
    TAG: str = ""

    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))

    id = int(ob['id'])
    Statement = str(ob['Statement'])
    ParentID = int(ob['ParentID'])
    TAG = str(ob['TAG'])

    id = int(ob['id'])

    sqlstring: str = "UPDATE fred.Product_Use_Case SET Statement = '" + Statement + "', ParentID = " + str(
        ParentID) + ", TAG = '" + TAG + "' WHERE id=" + str(id)
    print("Updating Store layout " + sqlstring)

    dac_code.db_sql_write(sqlstring)
