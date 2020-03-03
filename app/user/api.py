
from project.config_include.common import ServerUrl
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector

from app.cache.utils import RedisCaCheHandler
from app.user.serialiers import UsersModelSerializer,RoleModelSerializer
from app.user.models import Users,Role

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
                "avatar": ServerUrl+'/statics/images/pic.jpg',
                'roles': [ {"name":item.name,"rolecode":item.rolecode} for item in Role.objects.filter(rolecode__startswith='4')]
            },
            "roles": request.user.get("role").get("rolecode"),
            "permission": []
        }}

    @list_route(methods=['GET'])
    @Core_connector(isTicket=True,isPasswd=True,isPagination=True)
    def getUser(self, request):
        query = Users.objects.filter(rolecode__startswith='4')

        return {"data": UsersModelSerializer(query,many=True).data}


    @list_route(methods=['GET'])
    @Core_connector(isTicket=True,isPasswd=True,isPagination=True)
    def GetRole(self, request):
        query = Role.objects.filter(rolecode__startswith='4')

        return {"data": RoleModelSerializer(query,many=True).data}

    @list_route(methods=['POST'])
    @Core_connector(isTicket=True,isPasswd=True,isTransaction=True)
    def SaveRole(self, request):
        print(request.data_format)
        if not request.data_format.get("rolecode"):
            obj = Role.objects.filter(rolecode__startswith='4')
            rObj = [ int(item.rolecode) for item in obj ]
            maxRole = max(rObj)
            rolecode = str(maxRole + 1)

            Role.objects.create(**{
                "rolecode" : rolecode,
                "roletype":"4",
                "name":request.data_format.get("name")
            })
        else:
            Role.objects.filter(rolecode=request.data_format.get("rolecode")).update(name=request.data_format.get("name"))

        return None