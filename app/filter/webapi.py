
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector

from app.filter.menu import all_menu

from app.cache.utils import RedisCaCheHandler

from app.order.models import Order
from app.order.serialiers import OrderModelSerializer

from lib.utils.mytime import send_toTimestamp

class FilterWebAPIView(viewsets.ViewSet):
    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getMenu(self, request):
        """
        获取菜单数据
        :param request:
        :return:
        """

        type = self.request.query_params.get('type') if self.request.query_params.get("type") else "first"
        print(type)
        return {"data":all_menu[type]}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def getTopMenu(self, request):
        """
        获取顶部菜单数据
        :param request:
        :return:
        """

        return {"data":all_menu['top']}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getBanner(self, request):
        """
        获取轮播图图片
        :param request:
        :return:
        """

        data = RedisCaCheHandler(
            method="filter",
            serialiers="BannerModelSerializerToRedis",
            table="banner",
            filter_value=request.query_params_format
        ).run()

        return {"data": data}


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getOtherMemo(self, request):
        """
        获取公告数据
        :param request:
        :return:
        """

        obj =RedisCaCheHandler(
            method="filter",
            serialiers="OtherMemoModelSerializerToRedis",
            table="OtherMemo",
            filter_value=request.query_params_format
        ).run()
        print(obj)
        return {"data": obj[0] if obj else False}

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True, isTicket=True)
    def OrderGetWeb(self, request):

        orderQuery = Order.objects.filter()

        if request.query_params_format.get("status"):
            orderQuery = orderQuery.filter(status=request.query_params_format.get("status"))

        if request.query_params_format.get("fhstatus"):
            orderQuery = orderQuery.filter(fhstatus=request.query_params_format.get("fhstatus"))

        if request.query_params_format.get("userid"):
            orderQuery = orderQuery.filter(userid=request.query_params_format.get("userid"))

        if request.query_params_format.get("orderid"):
            orderQuery = orderQuery.filter(orderid=request.query_params_format.get("orderid"))

        if request.query_params_format.get("startdate") and request.query_params_format.get("enddate"):
            orderQuery = orderQuery.filter(
                createtime__lte=send_toTimestamp(request.query_params_format.get("enddate")),
                createtime__gte=send_toTimestamp(request.query_params_format.get("startdate")))

        page = int(request.query_params_format.get("page", 1))

        page_size = request.query_params_format.get("page_size", 10)
        page_start = page_size * page - page_size
        page_end = page_size * page

        res=orderQuery.order_by('-createtime')
        headers = {
            'Total': res.count(),
        }

        return {
            "data": OrderModelSerializer(res[page_start:page_end], many=True).data,
            "header":headers
        }