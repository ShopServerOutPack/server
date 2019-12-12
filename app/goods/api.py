
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from app.user.models import Users
from lib.utils.exceptions import PubErrorCustom

from app.cache.utils import RedisCaCheHandler

from app.goods.models import GoodsCateGory,Goods
from app.goods.serialiers import GoodsCateGoryModelSerializer,GoodsModelSerializer

class GoodsAPIView(viewsets.ViewSet):

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def openVip(self, request):
        """
        开通会员
        :param request:
        :return:
        """
        print(request.data_format)
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
            filter_value=request.query_params_format
        ).run()

        return {"data":obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isTicket=True,isPasswd=True)
    def delGoodsCategory(self,request,*args, **kwargs):

        print(request.data_format)
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
        obj.save()

        RedisCaCheHandler(
            method="save",
            serialiers="GoodsModelSerializerToRedis",
            table="goods",
            filter_value=obj,
            must_key="gdid",
        ).run()

        return None


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True,isPagination=True)
    def getGoods(self,request,*args, **kwargs):

        obj =RedisCaCheHandler(
            method="filter",
            serialiers="GoodsModelSerializerToRedis",
            table="goods",
            filter_value=request.query_params_format
        ).run()

        print(request.query_params_format)
        print(obj)

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