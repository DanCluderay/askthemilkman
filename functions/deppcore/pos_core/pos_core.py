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


def generic_insert_command(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    TableName: str = str(ob['TableName'])#THERE MUST BE A FEILD CALLED TableName
    Pk: str = str(ob['Pk'])  # THERE MUST BE A FEILD CALLED Pk
    #loop the dict
    nameparams=""
    valueparams=""

    for k, v in ob.items():
        print(k, v)
        temp:str=""
        if k == "TableName" or k == "Pk" or k == "UpDateWhere":
            print("found " + k)
        else:
            if nameparams=="":
                temp = k
                tempv = "'" + v + "'"
            else:
                temp = " ," + k
                tempv = " ,'" + v + "'"
            nameparams = nameparams + temp
            valueparams = valueparams + tempv

    fullstring="INSERT INTO fred." + TableName + " (" + nameparams + ") VALUES (" + valueparams + ")"
    print(fullstring)
    return dac_code.db_sql_write(fullstring)



def generic_update_command(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    TableName: str = str(ob['TableName'])#THERE MUST BE A FEILD CALLED TableName
    Pk: str = str(ob['Pk'])  # THERE MUST BE A FEILD CALLED Pk
    UpDateWhere: str = str(ob['UpDateWhere'])  # THERE MUST BE A FEILD CALLED UpDateWhere
    #loop the dict
    start_str="UPDATE fred." + TableName + " SET "
    param_str=""
    end_str=" WHERE " + str(TableName) + "." + str(Pk) + " = " + str(UpDateWhere)
    for k, v in ob.items():
        print(k, v)
        temp:str=""
        if k == "TableName" or k == "Pk" or k == "UpDateWhere":
            print("found " + k)
        else:
            if param_str=="":
                temp = k + "='" + str(v) + "' "
            else:
                temp = "," + k + "='" + str(v) + "' "
            param_str=param_str+temp

    fullstring=start_str + param_str + end_str
    print(fullstring)
    return dac_code.db_sql_write(fullstring)


def update_product_dataset(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    ProductID: str = str(ob['ProductID'])  # Check if its an insert or update by looking at if there is a ProductID

    if ProductID == "0":
        print("Performing product insert ProductID = " + str(ProductID))
        return generic_insert_command(para)
    else:
        print("Performing product Update ProductID = " + str(ProductID))
        return generic_update_command(para)

def get_product_barcode_by_brandproduct(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    BrandProductID: str = str(ob['BrandProductID'])
    sqlcode = "SELECT Product_Barcodes.ProductBarcodeID, Product_Barcodes.BrandProductID, Product_Barcodes.BarcodeType, Product_Barcodes.Barcode, Product_Barcodes.CaseQTY, Product_Barcodes.IsDeleted FROM fred.Product_Barcodes Product_Barcodes WHERE (Product_Barcodes.BrandProductID = " + str(BrandProductID) + ")"
    result = dac_code.dbreadquery_sql(sqlcode)

    return result


def get_brand_products_by_id(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    BrandID: str = str(ob['BrandID'])
    sqlcode = "SELECT Brand_Products.BrandProductID, Brand_Products.Brand, Brand_Products.ProductName FROM fred.Brand_Products Brand_Products WHERE (Brand_Products.Brand = " + BrandID + ")"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result

def add_new_brand_product(para):

    #pull out the parameters
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    Brand:str = str(ob['Brand'])
    ProductName: str = str(ob['ProductName'])
    GUID: str = uuid.uuid4()

    # Insert the new row
    sqlstring: str = "INSERT INTO fred.Brand_Products(Brand, ProductName, GUID) VALUES ('" + str(Brand) + "','" + str(ProductName) + "','" + str(GUID) + "');"
    dac_code.db_sql_write(sqlstring)

    #return the new primary key
    sqlcode = "SELECT Brand_Products.BrandProductID FROM fred.Brand_Products Brand_Products WHERE (Brand_Products.GUID = '" + str(GUID) + "')"
    result = dac_code.dbreadquery_sql(sqlcode)

    return result

def get_all_product_sizes():
    sqlcode = "SELECT Product_Size_Units.ID, Product_Size_Units.Unit, Product_Size_Units.`TheOrder`, Product_Size_Units.GroupType FROM fred.Product_Size_Units Product_Size_Units ORDER BY Product_Size_Units.GroupType ASC, Product_Size_Units.`TheOrder` ASC"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result

def add_new_product(para):

    #pull out the parameters
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    ProductName:str = str(ob['ProductName'])
    ProductType: str = str(ob['ProductType'])

    BrandID: str = str(ob['BrandID'])
    ProductShortDescription: str = str(ob['ProductShortDescription'])
    ProductFullName: str = str(ob['ProductFullName'])
    ProductRealWeight: str = str(ob['ProductRealWeight'])
    ProductLongDescription: str = str(ob['ProductLongDescription'])
    ProductVateCode: str = str(ob['ProductVateCode'])
    ProductVolumetricWeight: str = str(ob['ProductVolumetricWeight'])
    ProductRRP: str = str(ob['ProductRRP'])

    IsCasePick: str = str(ob['IsCasePick'])
    ProductLenght: str = str(ob['ProductLenght'])
    ProductWidth: str = str(ob['ProductWidth'])
    ProductHeight: str = str(ob['ProductHeight'])
    ProductTotalVolume: str = str(ob['ProductTotalVolume'])
    SizeID: str = str(ob['SizeID'])
    PreFix: str = str(ob['PreFix'])
    PostFix: str = str(ob['PostFix'])
    BrandInName: str = str(ob['BrandInName'])
    ISLocked: str = str(ob['ISLocked'])
    IsLockedBy: str = str(ob['IsLockedBy'])


    GUID: str = uuid.uuid4()

    # Insert the new row
    sqlstring: str = "INSERT INTO fred.Products(ProductName, ProductType, BrandID, ProductShortDescription, ProductFullName, ProductRealWeight, ProductLongDescription, ProductVateCode, ProductVolumetricWeight, ProductRRP, IsCasePick, ProductLenght, ProductWidth, ProductHeight, ProductTotalVolume, SizeID, PreFix, PostFix, BrandInName, ISLocked, IsLockedBy, GUID) VALUES ('" + str(ProductName) + "','" + str(ProductType) + "','" + str(BrandID) + "','" + str(ProductShortDescription) + "','" +  str(ProductFullName) + "','" +  str(ProductRealWeight) + "','" +  str(ProductLongDescription) + "','" +  str(ProductVateCode) + "','" +  str(ProductVolumetricWeight) + "','" + str(ProductRRP) + "','" + str(IsCasePick) + "','" + str(ProductLenght) + "','" + str(ProductWidth) + "','" + str(ProductHeight) + "','" + str(ProductTotalVolume) + "','" + str(SizeID) + "','" + str(PreFix) + "','" + str(PostFix) + "','" + str(BrandInName) + "','" + str(ISLocked) + "','" + str(IsLockedBy) + "','" + str(GUID) + ");"
    dac_code.db_sql_write(sqlstring)

    #return the new primary key
    sqlcode = "SELECT Products.ProductID, Products.GUID  FROM fred.Products Products WHERE (Products.GUID = '" + str(GUID) + "')"
    result = dac_code.dbreadquery_sql(sqlcode)

    return result

def get_product_from_id(para):
    # pull out the parameters
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    ProductID: str = str(ob['ProductID'])
    sqlcode = "SELECT Products.ProductID, Products.ProductName, Products.ProductType, Products.BrandID, Products.ProductShortDescription, Products.ProductFullName, Products.ProductRealWeight, Products.ProductLongDescription, Products.ProductVateCode, Products.ProductVolumetricWeight, Products.ProductRRP, Products.IsCasePick, Products.ProductLenght, Products.ProductWidth, Products.ProductHeight, Products.ProductTotalVolume, Products.SizeID, Products.PreFix, Products.PostFix, Products.BrandInName, Products.ISLocked, Products.IsLockedBy, Products.ProductImageURL, Products.GUID FROM fred.Products Products WHERE ProductID=" + ProductID
    result = dac_code.dbreadquery_sql(sqlcode)
    return result

def get_all_brands():
    sqlcode = "SELECT Brands.BrandId, Brands.BrandName, Brands.BrandWeight, Brands.GUID FROM fred.Brands Brands ORDER BY Brands.SortOrder DESC, Brands.BrandName ASC"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result



def add_new_brand(para):

    #pull out the parameters
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    BrandName:str = str(ob['BrandName'])
    BrandWeight: str = str(ob['BrandWeight'])
    GUID: str = uuid.uuid4()

    # Insert the new row
    sqlstring: str = "INSERT INTO fred.Brands(BrandName, BrandWeight, GUID) VALUES ('" + str(BrandName) + "','" + str(BrandWeight) + "','" + str(GUID) + "');"
    dac_code.db_sql_write(sqlstring)

    #return the new primary key
    sqlcode = "SELECT Brands.BrandID FROM fred.Brands Brands WHERE (Brands.GUID = '" + str(GUID) + "')"
    result = dac_code.dbreadquery_sql(sqlcode)

    return result

def update_brand(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    print(str(ob))
    BrandName:str = str(ob['BrandName'])
    BrandWeight: str = str(ob['BrandWeight'])
    BrandId: str = str(ob['BrandId'])

    #update the database
    sqlstring: str = "UPDATE fred.Brands SET BrandName ='" + str(BrandName) + "', BrandWeight ='" + str(BrandWeight) + "' WHERE Brands.BrandId=" + str(BrandId)
    dac_code.db_sql_write(sqlstring)



pass










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
