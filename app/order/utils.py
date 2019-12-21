
import requests,string,random,time
import hashlib
import json
import xmltodict

from project.config_include.params import WECHAT_PAY_KEY,WECHAT_APPID,CALLBACKURL,WECHAT_PAY_MCHID,WECHAT_PAY_RETURN_KEY
from lib.utils.exceptions import PubErrorCustom
from app.order.models import Order
from app.user.models import Users

class wechatPay(object):

    def __init__(self):

        self.createUrl = "https://api.mch.weixin.qq.com/pay/unifiedorder"

    def hashdata(self,data,key):

        res = self.sortKeyStringForDict(data,key)
        return hashlib.md5(res.encode('utf-8')).hexdigest().upper()

    def sortKeyStringForDict(self,data,key):
        strJoin = ""
        for item in sorted({k: v for k, v in data.items() if v != ""}):
            if item == 'sign':
                continue
            strJoin += "{}={}&".format(str(item), str(data[item]))
        strJoin += "key={}".format(key)
        print(strJoin)
        return strJoin

    def request(self,request_data):

        data={}

        data['appid'] = WECHAT_APPID
        data['mch_id'] = WECHAT_PAY_MCHID
        data['nonce_str'] = ''.join(random.sample(string.ascii_letters  + string.digits, 30))
        data['body'] = "商城系统-购买商品"
        data['out_trade_no'] = request_data['out_trade_no']
        data['total_fee'] = request_data['total_fee']
        data['spbill_create_ip'] = request_data['spbill_create_ip']
        data['notify_url'] = CALLBACKURL
        data['trade_type'] = 'JSAPI'
        data['openid'] = request_data['openid']
        data['sign_type'] = 'MD5'

        data['sign'] = self.hashdata(data,WECHAT_PAY_KEY)

        param = {'root': data}
        xml = xmltodict.unparse(param)

        res = requests.request(method="POST",data=xml.encode('utf-8'),url=self.createUrl,headers={'Content-Type': 'text/xml'})

        xmlmsg = xmltodict.parse(res.content.decode('utf-8'))

        if xmlmsg['xml']['return_code'] == 'SUCCESS':

            sign = self.hashdata(xmlmsg['xml'], WECHAT_PAY_KEY)

            if sign != xmlmsg['xml']['sign']:
                raise PubErrorCustom("非法操作！")

            prepay_id = xmlmsg['xml']['prepay_id']
            timeStamp = str(int(time.time()))

            data = {
                "appId": WECHAT_APPID,
                "nonceStr": data['nonce_str'],
                "package": "prepay_id=" + prepay_id,
                "signType": 'MD5',
                "timeStamp": timeStamp
            }
            data['paySign']=self.hashdata(data, WECHAT_PAY_KEY)

            data["orderid"] = request_data['out_trade_no']

            return data
        else:
            raise PubErrorCustom(xmlmsg['xml']['return_msg'])


    def callback(self,request):
        msg = request.body.decode('utf-8')
        xmlmsg = xmltodict.parse(msg)
        return_code = xmlmsg['xml']['return_code']

        print("腾讯支付回调数据:\n\t",xmlmsg['xml'])

        if return_code == 'SUCCESS':

            sign = self.hashdata(xmlmsg['xml'], WECHAT_PAY_KEY)
            if sign != xmlmsg['xml']['sign']:
                print(sign)
                raise Exception("非法操作！")

            if  xmlmsg['xml']['result_code'] == 'SUCCESS':
                out_trade_no = xmlmsg['xml']['out_trade_no']
                total_fee = xmlmsg['xml']['total_fee']


                order = Order.objects.select_for_update().get(orderid=out_trade_no)
                if float(order.amount)*100 != float(total_fee):
                    raise Exception("金额不一致")

                if order.status=='1':
                    raise Exception("该订单已支付!")

                order.paymsg = json.dumps(xmlmsg['xml'])
                order.status=1
                order.save()

                user = Users.objects.select_for_update().get(userid=order.userid)
                if float(order.balamount>0.0):
                    user.bal -= float(order.balamount)
                    user.save()
            else:
                raise Exception("error")
        else:
            raise Exception("error")

    def orderQuery(self,orderid):

        data={
            "appid":WECHAT_APPID,
            "mch_id":WECHAT_PAY_MCHID,
            "out_trade_no": orderid,
            "nonce_str":''.join(random.sample(string.ascii_letters  + string.digits, 30)),
            "sign_type":'MD5'
        }
        data['sign'] = self.hashdata(data, WECHAT_PAY_KEY)
        param = {'root': data}
        xml = xmltodict.unparse(param)
        res = requests.request(method="POST", data=xml.encode('utf-8'), url="https://api.mch.weixin.qq.com/pay/orderquery",
                               headers={'Content-Type': 'text/xml'})

        xmlmsg = xmltodict.parse(res.content.decode('utf-8'))

        if xmlmsg['xml']['return_code'] == 'SUCCESS':
            # sign = self.hashdata(xmlmsg['xml'], WECHAT_PAY_KEY)
            # print(sign)
            # print(xmlmsg['xml'])
            # if sign != xmlmsg['xml']['sign']:
            #     raise PubErrorCustom("非法操作！")

            if xmlmsg['xml']['result_code'] == 'SUCCESS':
                order = Order.objects.select_for_update().get(orderid=orderid)
                if order.status=='1':
                    return {"data": True}
                order.status = 1
                order.save()

                user = Users.objects.select_for_update().get(userid=order.userid)
                if float(order.balamount>0.0):
                    user.bal -= float(order.balamount)
                    user.save()
                return {"data": True}
            else:
                return {"data":False}
        else:
            return {"data":False}