
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector

from app.filter.menu import all_menu

from app.cache.utils import RedisCaCheHandler

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