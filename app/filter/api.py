
from rest_framework import viewsets
from rest_framework.decorators import list_route
import json

from lib.utils.exceptions import PubErrorCustom
from lib.core.decorator.response import Core_connector
from lib.utils.db import RedisCaCheHandlerCitySheng,RedisCaCheHandlerCityShi,RedisCaCheHandlerCityXian

from app.cache.utils import RedisCaCheHandler

from app.order.models import Address
from app.order.serialiers import AddressModelSerializer

from lib.utils.db import RedisTokenHandler

class FilterAPIView(viewsets.ViewSet):

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getHomeData(self,request):

        rolecode = None

        ticket = request.META.get('HTTP_TICKET')
        if ticket:
            result = RedisTokenHandler(key=ticket).redis_dict_get()
            if result:
                rolecode = result.get("rolecode")

        print("角色:[%s]"%rolecode)

        rdata={
            "banners":[],
            "category_hot":[],
            "category_tj": [],
            "newgoods":[]
        }

        #轮播图数据
        rdata['banners'] = [ dict(
            id = item['id'],
            url = item['url']
        ) for item in RedisCaCheHandler(
            method="filter",
            serialiers="BannerModelSerializerToRedis",
            table="banner",
            filter_value={}
        ).run() ]

        #主题分类数据(热门)
        rdata['category_hot'] = [  dict(
            typeid = item['typeid'],
            name = item['name'],
            sort = item['sort'],
            url  = item['url'],
            url1 = item['url1']
        ) for item in RedisCaCheHandler(
            method="filter",
            serialiers="GoodsThemeModelSerializerToRedis",
            table="goodstheme",
            filter_value={"status":"0","type":"0","rolecode":rolecode if rolecode else '4001'}
        ).run() ]
        rdata['category_hot'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)


        #主题分类数据(推荐)
        rdata['category_tj'] = [  dict(
            typeid = item['typeid'],
            name = item['name'],
            sort = item['sort'],
            url  = item['url'],
            url1=item['url1']
        ) for item in RedisCaCheHandler(
            method="filter",
            serialiers="GoodsThemeModelSerializerToRedis",
            table="goodstheme",
            filter_value={"status":"0","type":"1","rolecode":rolecode if rolecode else '4001'}
        ).run() ]
        rdata['category_tj'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        #新品数据


        for item in RedisCaCheHandler(
                method="filter",
                serialiers="GoodsModelSerializerToRedis",
                table="goods",
                filter_value={"gdstatus": "0"}
        ).run():
            obj = RedisCaCheHandler(
                method="get",
                serialiers="GoodsCateGoryModelSerializerToRedis",
                table="goodscategory",
                must_key_value=item.get('gdcgid')
            ).run()
            if obj['rolecode'] == rolecode or obj['rolecode'] == '4001':
                rdata['newgoods'].append(dict(
                    gdid=item['gdid'],
                    gdname=item['gdname'],
                    gdimg=item['gdimg'],
                    gdprice=item['gdprice'],
                    sort=item['sort']
                ))

        if len(rdata['newgoods']) >=6 :
            rdata['newgoods'] = rdata['newgoods'][:6]
        else:
            rdata['newgoods'] = rdata['newgoods'][:len(rdata['newgoods'])]
        rdata['newgoods'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        return {"data": rdata}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getGoods(self,request):

        res = RedisCaCheHandler(
            method="get",
            serialiers="GoodsModelSerializerToRedis",
            table="goods",
            must_key_value=request.query_params_format.get('gdid')
        ).run()
        if res['gdstatus'] == '0':
            return {
                "data":dict(
                    gdid = res['gdid'],
                    gdimg = res['gdimg'],
                    gdnum = res['gdnum'],
                    gdname = res['gdname'],
                    gdprice = res['gdprice'],
                    detail = res['detail'],
                    product = res['product'],
                    shbz = res['shbz'],
                    qrcode = res['qrcode'],
                    hb=res['hb']
                )
            }
        else:
            return {"data":False}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getGoodsForTheme(self,request):


        obj = RedisCaCheHandler(
            method="get",
            serialiers="GoodsThemeModelSerializerToRedis",
            table="goodstheme",
            must_key_value=request.query_params_format.get('typeid')
        ).run()

        if obj['status']=='0':
            goods = []
            for gdid in json.loads(obj['goods'])['goods']:
                res = RedisCaCheHandler(
                    method="get",
                    serialiers="GoodsModelSerializerToRedis",
                    table="goods",
                    must_key_value=gdid
                ).run()

                if res['gdstatus'] == '0':
                    goods.append(dict(
                        gdid=res['gdid'],
                        gdimg=res['gdimg'],
                        gdname=res['gdname'],
                        gdprice=res['gdprice'],
                        sort = res['sort']
                    ))
            goods.sort(key=lambda k: (k.get('sort', 0)), reverse=False)

            return {"data":goods}
        else:
            return {"data":False}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getGoodsForCategory(self,request):


        obj = RedisCaCheHandler(
            method="get",
            serialiers="GoodsCateGoryModelSerializerToRedis",
            table="goodscategory",
            must_key_value=request.query_params_format.get('gdcgid')
        ).run()

        if obj['status']=='0':
            goods = []

            res = RedisCaCheHandler(
                method="filter",
                serialiers="GoodsModelSerializerToRedis",
                table="goods",
                filter_value={"gdstatus": "0", "gdcgid":obj['gdcgid']}
            ).run()

            for item in res:
                goods.append(dict(
                    gdid=item['gdid'],
                    gdimg=item['gdimg'],
                    gdname=item['gdname'],
                    sort=item['sort']
                ))
            goods.sort(key=lambda k: (k.get('sort', 0)), reverse=False)
            return {"data":goods}
        else:
            return {"data":False}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getGoodsCategory(self,request,*args, **kwargs):

        """
        获取商品分类数据
        :param request:
        :return:
        """

        rolecode = None

        ticket = request.META.get('HTTP_TICKET')
        if ticket:
            result = RedisTokenHandler(key=ticket).redis_dict_get()
            if result:
                rolecode = result.get("rolecode")

        print("角色:[%s]" % rolecode)

        obj = [ dict(
            gdcgid = item['gdcgid'],
            gdcgname = item['gdcgname'],
            url = item['url'],
            sort = item['sort']
        ) for item in RedisCaCheHandler(
            method="filter",
            serialiers="GoodsCateGoryModelSerializerToRedis",
            table="goodscategory",
            filter_value={"status":"0","rolecode":rolecode if rolecode else '4001'}
        ).run() ]

        obj.sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        return {"data":obj}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getAddress(self,request):

        return {"data":AddressModelSerializer(Address.objects.filter(userid=request.user['userid']).order_by('moren','-createtime'),many=True).data}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getBanner(self, request):
        """
        获取轮播图
        :param request:
        :return:
        """

        data = RedisCaCheHandler(
            method="filter",
            serialiers="BannerModelSerializerToRedis",
            table="banner",
            filter_value=request.query_params_format
        ).run()

        return {"data":data}





    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getGoodsList(self, request):
        """
        获取商品数据
        :param request:
        :return:
        """
        objs=[]
        for item in request.query_params_format['goods']:
            objs.append(RedisCaCheHandler(
                method="get",
                serialiers="GoodsModelSerializerToRedis",
                table="goods",
                must_key_value=item
            ).run())
        return {"data":objs.sort(key=lambda k: (k.get('sort', 0)), reverse=False)}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getSheng(self, request):
        """
        获取省份数据
        :param request:
        :return:
        """
        res = RedisCaCheHandlerCitySheng().redis_get()
        return {"data":res['value']}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getShi(self, request):
        """
        获取市区数据
        :param request:
        :return:
        """
        if not request.query_params_format["code"]:
            raise PubErrorCustom("code不能为空!")
        res = RedisCaCheHandlerCityShi().redis_dict_get(request.query_params_format["code"])
        return {"data": res['value']}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getXian(self, request):
        """
        获取县数据
        :param request:
        :return:
        """
        if not request.query_params_format["code"]:
            raise PubErrorCustom("code不能为空!")
        res = RedisCaCheHandlerCityXian().redis_dict_get(request.query_params_format["code"])
        return {"data": res['value']}

