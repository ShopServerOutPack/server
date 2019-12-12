
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from lib.utils.exceptions import PubErrorCustom
from lib.utils.db import RedisTokenHandler
from lib.utils.string_extension import get_token
from lib.utils.http_request import send_request_other

from app.user.models import Users,Login
from app.cache.serialiers import UserModelSerializerToRedis
from app.cache.utils import RedisCaCheHandler

from lib.utils.WXBizDataCrypt import WXBizDataCrypt

from app.idGenerator import idGenerator
from lib.utils.txcloud import txCloud

from app.order.models import ShopCart
from app.order.serialiers import ShopCartModelSerializer

class SsoAPIView(viewsets.ViewSet):


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True)
    def wechatauth(self, request):
        params = dict(
            js_code=request.data_format.get("js_code"),
            appid="wx826e7da0c143bda7",
            secret="8e9e15e030441edc9eeccd934f43b1d4",
            grant_type="authorization_code",
        )
        res = send_request_other(
            url="https://api.weixin.qq.com/sns/jscode2session",
            params=params)
        if not res.get("openid"):
            raise PubErrorCustom("获取用户错误,腾讯接口有误!")
        print(res)
        try:
            data = UserModelSerializerToRedis(Users.objects.get(uuid=res.get('openid')),many=False).data
        except Users.DoesNotExist:
            data={}

        shopcart = ShopCartModelSerializer(ShopCart.objects.filter(userid=data.get("userid", 0)), many=True).data
        shopnumber = 0
        for item in shopcart:
            shopnumber += item['gdnum']

        return {"data":{
            "user" : data if data else {},
            "shopcart" :  shopcart,
            "shopnumber" : shopnumber,
            "session_key":res.get("session_key")
        }}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True)
    def wechatlogin(self, request):

        session_key = request.data_format.get("session_key")
        appId = 'wx826e7da0c143bda7'
        sessionKey = session_key
        encryptedData = request.data_format.get("encryptedData")
        iv = request.data_format.get("iv")

        pc = WXBizDataCrypt(appId, sessionKey)

        res = pc.decrypt(encryptedData, iv)

        try:
            obj = UserModelSerializerToRedis(Users.objects.get(uuid=res.get('openId') if 'unionId' not in res else res['unionId']),many=False).data
        except Users.DoesNotExist:
            user = Users.objects.create(**{
                "userid": idGenerator.userid('4001'),
                "uuid": res.get('openId') if 'unionId' not in res else res['unionId'],
                "rolecode": '4001',
                "name": res.get("nickName"),
                "sex": res.get("sex"),
                "addr": "{}-{}-{}".format(res.get("country"), res.get("city"), res.get("province")),
                "pic": res.get("avatarUrl"),
                "appid": res.get("watermark")['appid']
            })
            obj = RedisCaCheHandler(
                method="save",
                serialiers="UserModelSerializerToRedis",
                table="user",
                filter_value=user,
                must_key="userid",
            ).run()

        shopcart = ShopCartModelSerializer(ShopCart.objects.filter(userid=obj.get("userid",0)),many=True).data
        shopnumber = 0
        for item in shopcart:
            shopnumber += item['gdnum']

        return {"data":{
            "user" : obj,
            "shopcart" :  shopcart,
            "shopnumber" : shopnumber
        }}


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True)
    def login(self, request):

        try:
            user = Users.objects.get(uuid=request.data_format.get('username'))
        except Users.DoesNotExist:
            raise PubErrorCustom("登录账户错误！")

        if user.passwd != self.request.data_format.get('password'):
            raise PubErrorCustom("密码错误！")

        if user.status == 1:
            raise PubErrorCustom("登陆账号已到期！")
        elif user.status == 2:
            raise PubErrorCustom("已冻结！")
        token = get_token()
        res = UserModelSerializerToRedis(user, many=False).data
        RedisTokenHandler(key=token).redis_dict_set(res)

        return {"data": {
            "token": token
        }}

    #登出
    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True,isTicket=True)
    def logout(self,request, *args, **kwargs):

        RedisTokenHandler(key=request.ticket).redis_dict_del()
        return None

    #刷新token
    @list_route(methods=['POST'])
    @Core_connector(isPasswd=True,isTicket=True)
    def refeshToken(self,request, *args, **kwargs):

        redis_cli = RedisTokenHandler(key=request.ticket)
        res = redis_cli.redis_dict_get()
        redis_cli.redis_dict_del()

        token = get_token()
        redis_cli = RedisTokenHandler(key=token)
        redis_cli.redis_dict_set(res)

        return { "data": token}


    #获取腾讯云临时凭证
    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getAuthorization(self,request, *args, **kwargs):

        return { "data": txCloud().run()}