import boto3
import json
from session_vars import Singleton

keyp:str ="461824c0a06d4be0e94851deeabc3965"
passp:str  ="9bb4f551ba4888c9199b7a9509f0e872"
urlstart:str ="https://dans-daily-deals.myshopify.com/admin"

CURRENT_USERID = 0
CURRENT_ORDERID = 0
CURRENT_SESSIONID = ''
CURRENT_AMAZONID=''

def get_current_userid():
    return CURRENT_USERID

def set_current_userid(userid):
    CURRENT_USERID = userid
    return CURRENT_USERID

def mq(v):
    client = boto3.client('iot-data', region_name='eu-west-1', aws_access_key_id='AKIAJ35UPJ3TR23R56XA',
                          aws_secret_access_key='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')
    response = client.publish(
        topic='dancluderay',
        qos=1,
        payload=json.dumps({"msg": v})

    )

def getusername():
    gb=Singleton()
    print(gb.get_internal_userid())