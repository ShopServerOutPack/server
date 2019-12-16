
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.utils.exceptions import PubErrorCustom
from lib.core.decorator.response import Core_connector
from lib.utils.db import RedisCaCheHandlerCitySheng,RedisCaCheHandlerCityShi,RedisCaCheHandlerCityXian

from app.cache.utils import RedisCaCheHandler

from app.order.models import Address
from app.order.serialiers import AddressModelSerializer

class FilterAPIView(viewsets.ViewSet):

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getHomeData(self,request):

        rdata={
            "banners":[],
            "category_theme_one":[],  #一列
            "category_theme_two": [], #二列
            "newgoods":[]
        }

        #轮播图数据
        rdata['banners'] = RedisCaCheHandler(
            method="filter",
            serialiers="BannerModelSerializerToRedis",
            table="banner",
            filter_value={}
        ).run()

        #主题分类数据(一列)
        rdata['category_theme_one'] = RedisCaCheHandler(
            method="filter",
            serialiers="GoodsCateGoryModelSerializerToRedis",
            table="goodscategory",
            filter_value={"isstart":"0","istheme":"0","islie":"1"}
        ).run()

        rdata['category_theme_one'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        #主题分类数据(二列)
        rdata['category_theme_two'] = RedisCaCheHandler(
            method="filter",
            serialiers="GoodsCateGoryModelSerializerToRedis",
            table="goodscategory",
            filter_value={"isstart":"0","istheme":"0","islie":"0"}
        ).run()

        rdata['category_theme_two'].sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        #新品数据
        rdata['newgoods'] =RedisCaCheHandler(
            method="filter",
            serialiers="GoodsModelSerializerToRedis",
            table="goods",
                filter_value={"isnew":"0","gdstatus":"0"}
        ).run()

        return {"data": rdata}

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
    def getGoodsCategory(self,request,*args, **kwargs):

        """
        获取商品分类数据
        :param request:
        :return:
        """

        obj =RedisCaCheHandler(
            method="filter",
            serialiers="GoodsCateGoryModelSerializerToRedis",
            table="goodscategory",
            filter_value=request.query_params_format
        ).run()

        obj.sort(key=lambda k: (k.get('sort', 0)), reverse=False)

        return {"data":obj}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getGoodsList(self, request):
        """
        获取商品数据
        :param request:
        :return:
        """
        obj =RedisCaCheHandler(
            method="filter",
            serialiers="GoodsModelSerializerToRedis",
            table="goods",
            filter_value=request.query_params_format
        ).run()
        return {"data":obj}


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

