
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector

from app.cache.utils import RedisCaCheHandler
from app.user.serialiers import UsersModelSerializer
from app.user.models import Users

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
    @Core_connector(isTicket=True,isPasswd=True,isPagination=True)
    def getUser(self, request):
        query = Users.objects.filter(rolecode=request.query_params_format.get("rolecode"))

        return {"data": UsersModelSerializer(query,many=True).data}