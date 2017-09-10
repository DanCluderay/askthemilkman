import json
import lambda_function


eventstring="{'session': {'sessionId': 'SessionId.521b75f1-4d1c-4d9a-b068-96debbffbba9', 'application': {'applicationId': 'amzn1.ask.skill.3ce48dcb-8031-43ca-98a2-3f63ce2cbfaa'}, 'attributes': {}, 'user': {'userId': 'amzn1.ask.account.AGBI6UIAJIORPZLCDVIAOACMXHGO4IPHYPWTDZJSA4ASWDOXFBEV25F2UAH4OIXX2UXYZMMBP5ZMPETMAPA6CFUCTRXCKS6JZOQBOZ3YU2XOMEIPI6EMZYOT4KKHVK6XCJYS32ONDHTULJXJK5E3CVN4TU4E2WSCNMPUJBGY4MAV7ZOBJJEFM32IFJJLVSJJLKA24TGWSTVTIJA', 'accessToken': None}, 'new': False}, 'request': {'intent': {'name': 'WhatsMyName', 'slots': {}}, 'requestId': 'EdwRequestId.6a297441-ca7e-4bec-9093-0e446478498a', 'type': 'IntentRequest', 'locale': 'en-GB', 'timestamp': '2017-09-10T07:30:49Z'}, 'context': {'AudioPlayer': {'playerActivity': 'IDLE'}, 'System': {'application': {'applicationId': 'amzn1.ask.skill.3ce48dcb-8031-43ca-98a2-3f63ce2cbfaa'}, 'user': {'userId': 'amzn1.ask.account.AGBI6UIAJIORPZLCDVIAOACMXHGO4IPHYPWTDZJSA4ASWDOXFBEV25F2UAH4OIXX2UXYZMMBP5ZMPETMAPA6CFUCTRXCKS6JZOQBOZ3YU2XOMEIPI6EMZYOT4KKHVK6XCJYS32ONDHTULJXJK5E3CVN4TU4E2WSCNMPUJBGY4MAV7ZOBJJEFM32IFJJLVSJJLKA24TGWSTVTIJA'}, 'device': {'supportedInterfaces': {}}}}, 'version': '1.0'}"
lp = json.dumps(eventstring)
event=json.loads(lp)
context="<__main__.LambdaContext object at 0x7f06e2113f60>"

lambda_function.lambda_handler(eventstring,context)

