import requests
import json
from dac import dac_code

def pay_auth():
    username:str="hJYxsw7HLbj40cB8udES8CDRFLhuJ8G54O6rDpUXvE6hYDrria"
    password:str="o2iHSrFybYMZpmWOQMuhsXP52V4fBtpuSDshrKDSWsBY1OiN6hwd9Kb12z4j5Us5u"
    url:str="https://pi-test.sagepay.com/api/v1/merchant-session-keys/"
    body={"vendorName":"sandbox"}
    head = {"Content-type": "application/json",
               "Authorization": "Basic aEpZeHN3N0hMYmo0MGNCOHVkRVM4Q0RSRkxodUo4RzU0TzZyRHBVWHZFNmhZRHJyaWE6bzJpSFNyRnliWU1acG1XT1FNdWhzWFA1MlY0ZkJ0cHVTRHNocktEU1dzQlkxT2lONmh3ZDlLYjEyejRqNVVzNXU="}
    ret=requests.post(url,json=body,auth=(username,password),headers=head)
    d:dict=json.loads(ret.text)
    merchant_session:str=str(d.get("merchantSessionKey"))
    merchant_expiry:str=str(d.get("expiry"))
    print(str(merchant_session))
    print(str(merchant_expiry))
    return d

def sage_generateCI(merchantSessionKey):
    merchant_session: str = str(merchantSessionKey.get("merchantSessionKey"))
    url: str = "https://pi-test.sagepay.com/api/v1/card-identifiers/"
    body = {"cardDetails": {"cardholderName": "Card Holder","cardNumber": "4929000000006","expiryDate": "1120","securityCode": "123"}}
    head = {"Content-type": "application/json",
            "Authorization": "Bearer " + str(merchant_session) + ""}
    ret = requests.post(url, json=body, headers=head)

    d: dict = json.loads(ret.text)
    cardid: str = str(d.get("cardIdentifier"))
    print(cardid)
    return cardid

def sage_process_transaction(merchantSessionKey,cardid,orderid):
    merchant_session: str = str(merchantSessionKey.get("merchantSessionKey"))
    username: str = "hJYxsw7HLbj40cB8udES8CDRFLhuJ8G54O6rDpUXvE6hYDrria"
    password: str = "o2iHSrFybYMZpmWOQMuhsXP52V4fBtpuSDshrKDSWsBY1OiN6hwd9Kb12z4j5Us5u"
    url: str = "https://pi-test.sagepay.com/api/v1/transactions/"

    body = {"paymentMethod": { "card": { "merchantSessionKey": str(merchant_session) , "cardIdentifier": str(cardid) } }, "transactionType":"Payment", "vendorTxCode":str(orderid), "amount":2000, "currency":"GBP", "customerFirstName":"Sam", "customerLastName":"Jones", "billingAddress":{ "address1":"407 St. John Street", "city":"London", "postalCode":"EC1V 4AB", "country":"GB" }, "entryMethod":"Ecommerce", "apply3DSecure":"Disable", "applyAvsCvcCheck":"Disable", "description":"Testing", "customerEmail":"test.emaili@domain.com", "customerPhone":"0845 111 4455", "shippingDetails":{ "recipientFirstName":"Sam", "recipientLastName":"Jones", "shippingAddress1":"407 St John Street", "shippingCity":"London", "shippingPostalCode":"EC1V 4AB", "shippingCountry":"GB" } }

    head = {"Content-type": "application/json","Authorization": "Basic aEpZeHN3N0hMYmo0MGNCOHVkRVM4Q0RSRkxodUo4RzU0TzZyRHBVWHZFNmhZRHJyaWE6bzJpSFNyRnliWU1acG1XT1FNdWhzWFA1MlY0ZkJ0cHVTRHNocktEU1dzQlkxT2lONmh3ZDlLYjEyejRqNVVzNXU="}

    ret = requests.post(url, json=body,auth=(username,password), headers=head)
    retstr = ret.text
    print(retstr)
    d: dict =json.loads(retstr)

    sagetx_id: str = str(d.get("transactionId"))
    print(sagetx_id)
    return sagetx_id

def sage_process_repeat_transaction(ref_trans,neworderid,amount):
    '''Make a repeat purchase'''

    username: str = "hJYxsw7HLbj40cB8udES8CDRFLhuJ8G54O6rDpUXvE6hYDrria"
    password: str = "o2iHSrFybYMZpmWOQMuhsXP52V4fBtpuSDshrKDSWsBY1OiN6hwd9Kb12z4j5Us5u"
    url: str = "https://pi-test.sagepay.com/api/v1/transactions/"

    body = { "transactionType":"Repeat", "referenceTransactionId": str(ref_trans), "vendorTxCode":str(neworderid), "amount":amount, "currency":"GBP", "description":"Great product repeated", "shippingDetails":{ "recipientFirstName":"Sam", "recipientLastName":"Jones", "shippingAddress1":"407 St John Street", "shippingCity":"London", "shippingPostalCode":"EC1V 4AB", "shippingCountry":"GB" } }

    head = {"Content-type": "application/json",
            "Authorization": "Basic aEpZeHN3N0hMYmo0MGNCOHVkRVM4Q0RSRkxodUo4RzU0TzZyRHBVWHZFNmhZRHJyaWE6bzJpSFNyRnliWU1acG1XT1FNdWhzWFA1MlY0ZkJ0cHVTRHNocktEU1dzQlkxT2lONmh3ZDlLYjEyejRqNVVzNXU="}
    print(body)
    ret = requests.post(url, json=body, auth=(username, password), headers=head)
    print(ret)

def proccess_collections():
    #get a list of all transactions that are pending collection
    sqlstring="SELECT collections.id, collections.Customerid, collections.amount, collections.repeat_transactionID, collections.Parent_transaction, collections.date_due, collections.transaction_status, collections.status_string, collections.orderid FROM fred.collections collections WHERE (collections.date_due < '2017-09-01 00:00:00') AND (collections.transaction_status = 0)"
    res=dac_code.dbreadquery_sql(sqlstring)
    customerid:int=0
    amount:float=0.0
    Parent_transaction:str=""
    repeat_transactionID:str=""
    transaction_status:int=0
    for i in range(len(res)):
        rec:dict=i
        customerid=rec.get('Customerid',0)
        amount=rec.get('amount',0.0)
        Parent_transaction = rec.get('Parent_transaction','')
        repeat_transactionID = rec.get('repeat_transactionID','')
        transaction_status = rec.get('transaction_status',0)


    return 1

def create_new_customer_collection():
    #get customer details - ID, Billing date, card token, previous succesfull transaction and shipping address
    trans_data:dict={}
    trans_data['customerid']=1
    trans_data['Fname']='dan'
    trans_data['Sname'] = 'cluderay'
    trans_data['AddressLine1'] = '80 long lane'
    trans_data['City'] = 'Notts'
    trans_data['Postcode'] = 's819ar'
    trans_data['Country'] = 'GB'
    trans_data['billingday']='FRIDAY'
    trans_data['PST']='hksahkdakjsdhkasd'
    trans_data['parenttransaction'] = 1

    trans_data['cardtoken'] = '12312312332'


    #calculate the billing date based on day of week
    trans_data['billingdate'] = '2017-9-01'



    #get order - goods total, orderid
    trans_data['orderid'] = '101'
    trans_data['amount'] = 10

    sql="INSERT INTO `collections`(`Customerid`, `amount`, `referenceTransactionId`, `date_due`, `Parent_transaction`, `transaction_status`, `status_string`, `orderid`, `cardtoken`, `tranactiontype`, `currency`, `transdescription`, `recipientFirstName`, `recipientLastName`, `shippingAddress1`, `shippingCity`, `shippingPostalCode`, `shippingCountry`)    " \
        "VALUES('" + str(trans_data.get('customerid')) + "','" + str(trans_data.get('amount')) + "','" + str(trans_data.get('PST')) + "','" + str(trans_data.get('billingdate')) + "', '" + str(trans_data.get('parenttransaction')) + "', '1', 'PENDING', '" + str(trans_data.get('orderid')) + "', '" + str(trans_data.get('cardtoken')) + "', 'Repeat', 'GBP', 'food','" + str(trans_data.get('Fname')) + "','" + str(trans_data.get('Sname')) + "','" + str(trans_data.get('AddressLine1')) + "','" + str(trans_data.get('City')) + "','" + str(trans_data.get('Postcode')) + "','" + str(trans_data.get('Country')) + "')"
    print(sql)

    return 1