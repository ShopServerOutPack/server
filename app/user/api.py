
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector

from app.cache.utils import RedisCaCheHandler

class UserAPIView(viewsets.ViewSet):

    @list_route(methods=['GET'])
    @Core_connector(isTicket=True,isPasswd=True)
    def getUserInfo(self, request):

        return {"data": {
            "userInfo": {
                "username": request.user.get("uuid"),
                "name": request.user.get("name"),
                'rolecode': request.user.get("role").get("rolecode"),
                "rolename": request.user.get("role").get("rolename"),
                "avatar": 'http://allwin6666.com/nginx_upload/assets/login.jpg'
            },
            "roles": request.user.get("role").get("rolecode"),
            "permission": []
        }}

    @list_route(methods=['GET'])
    @Core_connector(isTicket=True,isPasswd=True)
    def getUser(self, request):

        data = RedisCaCheHandler(
            method="filter",
            serialiers="UserModelSerializerToRedis",
            table="user",
            filter_value=request.query_params_format,
            must_params=['rolecode']
        ).run()
        print(data)
        return {"data": data}