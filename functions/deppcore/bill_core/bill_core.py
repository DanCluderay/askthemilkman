import dac_code
import com_msg
import json
import random
import shopify
import requests
import uuid


def bill_update_brands(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    brands_ID: str = str(ob['brands_ID'])  # Check if its an insert or update by looking at if there is a ProductID
    if brands_ID == "0":
        print("Performing brands insert = " + str(brands_ID))
        return generic_insert_command_with_GUID(para)
    else:
        print("Performing brands update = " + str(brands_ID))
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
    fullstring="INSERT INTO fred." + TableName + " (" + nameparams + ") VALUES (" + valueparams + ")"
    print(fullstring)
    dac_code.db_sql_write(fullstring)
    sqlcode = "SELECT " + TableName + "." + Pk + " FROM fred." + TableName + " " + TableName + " WHERE (" + TableName + ".GUID = '" + str(GUID) + "')"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result

def generic_update_command(para):
    quoteless = para.replace("\'", "\"")
    ob: dict = json.loads(quoteless)
    TableName: str = str(ob['TableName'])  # THERE MUST BE A FEILD CALLED TableName
    Pk: str = str(ob['Pk'])  # THERE MUST BE A FEILD CALLED Pk
    UpDateWhere: str = str(ob['UpDateWhere'])  # THERE MUST BE A FEILD CALLED UpDateWhere
    # loop the dict
    start_str = "UPDATE fred." + TableName + " SET "
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
    res = dac_code.db_sql_write(fullstring)
    if res == 1:
        returnstring: dict = {'result': 1}
    else:
        returnstring: dict = {'result': 0}
    return returnstring