
import json,random
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from app.user.models import Users
from lib.utils.exceptions import PubErrorCustom

from app.user.models import Role

from app.cache.utils import RedisCaCheHandler
from lib.utils.db import RedisCaCheHandlerBase
from app.goods.models import GoodsCateGory,Goods,GoodsTheme,Card,Cardvirtual,DeliveryCode
from app.goods.serialiers import GoodsCateGoryModelSerializer,GoodsModelSerializer,\
    GoodsThemeModelSerializer,CardModelSerializer,CardvirtualModelSerializer,DeliveryCodeModelSerializer

class GoodsAPIView(viewsets.ViewSet):

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def openVip(self, request):
        """
        开通会员
        :param request:
        :return:
        """
        try:
            user = Users.objects.get(userid=request.user.get("userid"))
            user.isvip = 1
            user.save()
        except Users.DoesNotExist:
            raise PubErrorCustom("用户不存在!")
        return {"data":user.isvip}

        # return  {"data":RecursionForModle(
        #     headObj=GoodsCateGory.objects.get(gdcgid=1),
        #     queryNumber=99,
        #     objModle=GoodsCateGory,
        #     idKey='gdcgid',
        #     idLastKey="gdcglastid",
        #     serialiers=GoodsCateGoryModelSerializer).run()}


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=GoodsCateGoryModelSerializer,
                    model_class=GoodsCateGory)
    def saveGoodsCategory(self, request,*args,**kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()
        obj.userid = request.user.get('userid')
        obj.save()

        RedisCaCheHandler(
            method="save",
            serialiers="GoodsCateGoryModelSerializerToRedis",
            table="goodscategory",
            filter_value=obj,
            must_key="gdcgid",
        ).run()

        return None


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True,isPagination=True)
    def getGoodsCategory(self,request,*args, **kwargs):

        obj =RedisCaCheHandler(
            method="filter",
            serialiers="GoodsCateGoryModelSerializerToRedis",
            table="goodscategory",
            filter_value=request.query_params_format.get("filter_value",{}),
            condition_params=request.query_params_format.get("condition_params",[]),
        ).run()
        for item in obj:
            item['rolecode'] = json.loads(item['rolecode'])['rolecode']
            goods=[]
            for gdid in json.loads(item['goods'])['goods']:
                goods.append(RedisCaCheHandler(
                    method="get",
                    serialiers="GoodsModelSerializerToRedis",
                    table="goods",
                    must_key_value=gdid
                ).run())
            item['goods'] = goods
        return {"data":obj}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True)
    def getGoodsCategorys(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="GoodsCateGoryModelSerializerToRedis",
            table="goodscategory",
            filter_value=request.query_params_format
        ).run()

        return {"data":obj}


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isTicket=True,isPasswd=True)
    def delGoodsCategory(self,request,*args, **kwargs):

        GoodsCateGory.objects.filter(gdcgid=request.data_format.get('gdcgid')).delete()

        RedisCaCheHandler(
            method="delete",
            table="goodscategory",
            must_key_value=request.data_format.get('gdcgid')).run()

        return None

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=GoodsModelSerializer,
                    model_class=Goods)
    def saveGoods(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()
        obj.userid = request.user.get('userid')
        if obj.virtual == '0':
            if request.data_format.get("xuni"):
                obj.gdnum += len(request.data_format.get("xuni"))

                for item in request.data_format.get("xuni"):
                    Cardvirtual.objects.create(**{
                        "userid":request.user.get('userid'),
                        "account":item.get("card"),
                        "password":item.get("password"),
                        "gdid":obj.gdid
                    })
        obj.save()

        if obj.code == '0':
            if request.data_format.get("thm"):

                if int(request.data_format.get("thm").get("number",0))>0:

                    for item in range(int(request.data_format.get("thm").get("number",0))):

                        a = "0123456789abcdefghijklmnopqrstuvwxyz"

                        while True:
                            account = ""
                            for item in range(12):
                                account += random.choice(a)
                            if DeliveryCode.objects.filter(account=account).count() <= 0:
                                break

                        DeliveryCode.objects.create(**{
                            "account":account,
                            "userid": request.user.get('userid'),
                            "bal": request.data_format.get("thm").get("bal",0.0),
                            "gdid": obj.gdid,
                            "rolecode":request.data_format.get("thm").get("rolecode",""),
                            "rolename":Role.objects.get(rolecode=request.data_format.get("thm").get("rolecode","")).name
                        })

        RedisCaCheHandler(
            method="save",
            serialiers="GoodsModelSerializerToRedis",
            table="goods",
            filter_value=obj,
            must_key="gdid",
        ).run()

        return {"data":{"gdid":obj.gdid,"qrcode":obj.qrcode}}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True,isPagination=True)
    def getDeliveryCode(self,request,*args, **kwargs):
        print(request.query_params_format)
        queryObj = DeliveryCode.objects.filter(gdid=request.query_params_format.get("gdid"))

        if request.query_params_format.get("rolecode",None):
            queryObj = queryObj.filter(rolecode=request.query_params_format.get("rolecode",None))

        return {"data": DeliveryCodeModelSerializer(queryObj.order_by('-createtime'),many=True).data}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True,isPagination=True)
    def getGoodsVirtual(self,request,*args, **kwargs):

        queryObj = Cardvirtual.objects.filter(gdid=request.query_params_format.get("gdid"))

        return {"data": CardvirtualModelSerializer(queryObj,many=True).data}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True,isPagination=True)
    def getGoods(self,request,*args, **kwargs):

        obj =RedisCaCheHandler(
            method="filter",
            serialiers="GoodsModelSerializerToRedis",
            table="goods",
            filter_value=request.query_params_format
        ).run()

        if obj:
            RClass = RedisCaCheHandlerBase(key="goodscategory")
            for item in obj:
                print(item)
                res = RClass.redis_dict_get(item.get("gdcgid"))
                if res:
                    item['gdcgname'] = res['gdcgname']

        return {"data":obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isTicket=True,isPasswd=True)
    def delGoods(self,request,*args, **kwargs):

        print(request.data_format)
        Goods.objects.filter(gdid=request.data_format.get('gdid')).delete()

        RedisCaCheHandler(
            method="delete",
            table="goods",
            must_key_value=request.data_format.get('gdid')).run()

        return None

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True,
                    serializer_class=GoodsThemeModelSerializer,
                    model_class=GoodsTheme)
    def saveGoodsTheme(self, request, *args, **kwargs):

        serializer = kwargs.pop("serializer")
        obj = serializer.save()
        obj.userid = request.user.get('userid')
        obj.save()

        RedisCaCheHandler(
            method="save",
            serialiers="GoodsThemeModelSerializerToRedis",
            table="goodstheme",
            filter_value=obj,
            must_key="typeid",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getGoodsTheme(self, request, *args, **kwargs):

        print(request.query_params_format.get("filter_value",{}))
        obj = RedisCaCheHandler(
            method="filter",
            serialiers="GoodsThemeModelSerializerToRedis",
            table="goodstheme",
            filter_value=request.query_params_format.get("filter_value",{}),
            condition_params=request.query_params_format.get("condition_params",[]),
        ).run()
        for item in obj:
            item['rolecode'] = json.loads(item['rolecode'])['rolecode']
            goods = []
            for gdid in json.loads(item['goods'])['goods']:
                goods.append(RedisCaCheHandler(
                    method="get",
                    serialiers="GoodsModelSerializerToRedis",
                    table="goods",
                    must_key_value=gdid
                ).run())
            item['goods'] = goods
        return {"data": obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delGoodsTheme(self, request, *args, **kwargs):

        GoodsTheme.objects.filter(typeid=request.data_format.get('typeid')).delete()

        RedisCaCheHandler(
            method="delete",
            table="goodstheme",
            must_key_value=request.data_format.get('typeid')).run()

        return None

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True)
    def saveCard(self, request, *args, **kwargs):

        cards = []
        print(request.data_format)
        for item in range(int(request.data_format.get("number"))):
            cards.append(Card.objects.create(**{
                "userid" : request.user['userid'],
                "type": request.data_format.get("type"),
                "bal" : request.data_format.get("bal"),
                "rolecode" : request.data_format.get("rolecode")
            }))

        for item in cards:
            RedisCaCheHandler(
                method="save",
                serialiers="CardModelSerializerToRedis",
                table="card",
                filter_value=item,
                must_key="id",
            ).run()

        return None


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,
                    isPasswd=True,
                    isTicket=True)
    def saveCard1(self, request, *args, **kwargs):

        card = Card.objects.create(**{
            "userid": request.user['userid'],
            "type": request.data_format.get("type"),
            "account" : request.data_format.get("account"),
            "password": request.data_format.get("password"),
        })

        RedisCaCheHandler(
            method="save",
            serialiers="CardModelSerializerToRedis",
            table="card",
            filter_value=card,
            must_key="id",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True, isPagination=True)
    def getCard(self, request, *args, **kwargs):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="CardModelSerializerToRedis",
            table="card",
            filter_value=request.query_params_format
        ).run()
        return {"data": obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delCard(self, request, *args, **kwargs):

        Card.objects.filter(id=request.data_format.get('id')).delete()

        RedisCaCheHandler(
            method="delete",
            table="card",
            must_key_value=request.data_format.get('id')).run()

        return None

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isTicket=True, isPasswd=True)
    def delBatchCard(self, request, *args, **kwargs):

        cards = Card.objects.filter(id__in=request.data_format.get('ids'))
        cards.delete()

        for item in request.data_format.get('ids'):
            RedisCaCheHandler(
                method="delete",
                table="card",
                must_key_value=item).run()

        return None