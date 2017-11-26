import bill_dac
import com_msg
import json
import random
import shopify
import requests
import uuid


def bill_generic_select(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    TableName: str = str(ob['TableName'])  # THERE MUST BE A FEILD CALLED TableName
    Pk: str = str(ob['Pk'])  # THERE MUST BE A FEILD CALLED Pk
    UpDateWhere: str = str(ob['UpDateWhere'])  # THERE MUST BE A FEILD CALLED Pk
    # loop the dict
    selectparams = ""


    for k, v in ob.items():
        print(k, v)
        temp: str = ""
        if k == "TableName" or k == "Pk" or k == "UpDateWhere":
            print("found " + k)
        else:
            if selectparams == "":
                selectparams=TableName + "." + v
            else:
                temp = " ," + k
                selectparams =selectparams + " , " + TableName + "." + v



    sqlcode = "SELECT " + selectparams + " FROM bill." + TableName + " WHERE (" + Pk + " = " + UpDateWhere + ")"
    result = bill_dac.dbreadquery_sql(sqlcode)
    return result

def bill_generic_update_check(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    UpDateWhere: str = str(ob['UpDateWhere'])  # Check if its an insert or update by looking at if there is a ProductID
    if UpDateWhere == "0":
        print("Performing generic insert = " + str(UpDateWhere))
        return generic_insert_command_with_GUID(para)
    else:
        print("Performing generic update = " + str(UpDateWhere))
        return generic_update_command(para)

def generic_insert_command_with_GUID(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    TableName: str = str(ob['TableName'])#THERE MUST BE A FEILD CALLED TableName
    Pk: str = str(ob['Pk'])  # THERE MUST BE A FEILD CALLED Pk
    #loop the dict
    nameparams=""
    valueparams=""
    GUID: str = str(uuid.uuid4())
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
    nameparams = nameparams + " ,GUID"
    valueparams = valueparams + " ,'" + GUID + "'"

    nameparams = nameparams + " ,CreatedDateTime"
    valueparams = valueparams + " , Now()"

    nameparams = nameparams + " ,UpdatedDateTime"
    valueparams = valueparams + " , Now()"
    fullstring="INSERT INTO bill." + TableName + " (" + nameparams + ") VALUES (" + valueparams + ")"
    print(fullstring)
    bill_dac.db_sql_write(fullstring)
    sqlcode = "SELECT " + TableName + "." + Pk + " FROM bill." + TableName + " " + TableName + " WHERE (" + TableName + ".GUID = '" + str(GUID) + "')"
    result = bill_dac.dbreadquery_sql(sqlcode)
    returnid:int=0

    #convert from json to dict
    quoteless = str(result).replace("\'", "\"")
    #quoteless = str(result).replace("[", "")
    #quoteless = str(result).replace("]", "")
    ob: dict = json.loads(quoteless)
    print("results 2 " + str(ob))
    for key, value in ob[0].items():
        print("dict loop k=" + str(key) + " v=" + str(value))
        returnid=value

    return returnid


def generic_update_command(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    TableName: str = str(ob['TableName'])  # THERE MUST BE A FEILD CALLED TableName
    Pk: str = str(ob['Pk'])  # THERE MUST BE A FEILD CALLED Pk
    UpDateWhere: str = str(ob['UpDateWhere'])  # THERE MUST BE A FEILD CALLED UpDateWhere
    # loop the dict
    start_str = "UPDATE bill." + TableName + " SET "
    param_str = ""
    end_str = " WHERE " + str(TableName) + "." + str(Pk) + " = " + str(UpDateWhere)
    for k, v in ob.items():
        print(k, v)
        temp: str = ""
        if k == "TableName" or k == "Pk" or k == "UpDateWhere":
            print("found " + k)
        else:
            if param_str == "":
                temp = k + "='" + str(v) + "' "
            else:
                temp = "," + k + "='" + str(v) + "' "
            param_str = param_str + temp


    param_str = param_str + ", UpdatedDateTime= Now()"
    fullstring = start_str + param_str + end_str
    print(fullstring)
    res = bill_dac.db_sql_write(fullstring)
    if res == 1:
        print(UpDateWhere)
        print(str(UpDateWhere).replace("'",""))
        returnstring=int(UpDateWhere)
    else:
        returnstring=0
    return returnstring

#bill_generic_select("{'TableName':'product_varient_location_stock_qty','Pk':'product_varient_location_stock_qty_ID','UpDateWhere':'1','product_varient_location_stock_qty_ID':'product_varient_location_stock_qty_ID','product_instance_ID':'product_varient_location_stock_qty_ID','product_varient_location_ID':'product_varient_location_ID'}")