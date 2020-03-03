

import os

# #腾讯对象存储
# TX_SECRET_ID = os.getenv("TX_SECRET_ID",None)
# TX_SECRET_KEY = os.getenv("TX_SECRET_KEY",None)


import os

BASEURL = os.getenv("BASEURL","http://localhost:9006")
APIURL = "{}{}".format(BASEURL,"/v1/api")
CALLBACKURL = "{}{}".format(APIURL,"/order/txPayCallback")

#小程序
WECHAT_APPID = os.getenv("WECHAT_APPID",None)
WECHAT_SECRET = os.getenv("WECHAT_SECRET",None)
WECHAT_PAY_MCHID = os.getenv("WECHAT_PAY_MCHID",None)
WECHAT_PAY_KEY = os.getenv("WECHAT_PAY_KEY",None)
WECHAT_PAY_RETURN_KEY = os.getenv("WECHAT_PAY_RETURN_KEY",None)
