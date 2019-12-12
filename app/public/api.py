from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector

from lib.utils.exceptions import PubErrorCustom

from app.public.models import Banner,AttachMent,AttachMentGroup,OtherMemo
from app.cache.utils import RedisCaCheHandler

class PublicAPIView(viewsets.ViewSet):

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True)
    def setBanner(self, request):

        if len(request.data_format.get("banner")) > 5:
            raise PubErrorCustom("轮播图不允许超过5张!")

        Banner.objects.filter().delete()

        insertList=[]
        for item in request.data_format.get("banner"):
            res = Banner.objects.create(url=item.get('url'))
            insertList.append(res)

        RedisCaCheHandler(
            method="saveAll",
            serialiers="BannerModelSerializerToRedis",
            table="banner",
            filter_value=insertList,
            must_key="id",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getAttachMentGroup(self, request):

        obj = RedisCaCheHandler(
            method="filter",
            serialiers="AttachMentGroupModelSerializerToRedis",
            table="AttachMentGroup",
            filter_value=request.query_params_format
        ).run()

        return {"data":obj}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isPasswd=True)
    def setAttachMentGroup(self, request):

        if request.data_format.get("id"):
            obj = AttachMentGroup.objects.get(id= request.data_format.get("id"))
            obj.name = request.data_format.get("name")
            obj.save()
        else:
            obj = AttachMentGroup.objects.create(name=request.data_format.get('name'))

        RedisCaCheHandler(
            method="save",
            serialiers="AttachMentGroupModelSerializerToRedis",
            table="AttachMentGroup",
            filter_value=obj,
            must_key="id",
        ).run()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True)
    def getAttachMent(self, request):
        print(request.query_params_format)
        obj = RedisCaCheHandler(
            method="filter",
            serialiers="AttachMentModelSerializerToRedis",
            table="AttachMent",
            filter_value=request.query_params_format
        ).run()

        return {"data":obj}


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isPasswd=True)
    def setAttachMent(self, request):

        if request.data_format.get("id"):
            obj = AttachMent.objects.get(id= request.data_format.get("id"))
            obj.title = request.data_format.get("title")
            obj.grouid =  request.data_format.get("grouid")
            obj.save()
        else:
            obj = AttachMent.objects.create(**dict(
                url = request.data_format.get("url"),
                title = request.data_format.get("title"),
                grouid = request.data_format.get("grouid"),
                type = request.data_format.get("type")
            ))

            obj1 = AttachMentGroup.objects.select_for_update().get(id= obj.grouid)
            obj1.number +=1
            obj1.save()

        RedisCaCheHandler(
            method="save",
            serialiers="AttachMentGroupModelSerializerToRedis",
            table="AttachMentGroup",
            filter_value=obj1,
            must_key="id",
        ).run()

        RedisCaCheHandler(
            method="save",
            serialiers="AttachMentModelSerializerToRedis",
            table="AttachMent",
            filter_value=obj,
            must_key="id",
        ).run()

        return {"data":{
            "id":obj.id,
            "url":obj.url
        }}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isPasswd=True)
    def delAttachMent(self, request):

        print(request.data_format.get("id"))
        aObj = AttachMent.objects.filter(id=request.data_format.get("id"))
        if not aObj.exists():
            raise PubErrorCustom("不存在此照片!")
        else:
            obj=aObj[0]
            obj1 = AttachMentGroup.objects.select_for_update().get(id= obj.grouid)
            obj1.number -=1
            obj1.save()
            aObj.delete()

            RedisCaCheHandler(
                method="save",
                serialiers="AttachMentGroupModelSerializerToRedis",
                table="AttachMentGroup",
                filter_value=obj1,
                must_key="id",
            ).run()

            RedisCaCheHandler(
                method="delete",
                table="AttachMent",
                must_key="id",
                must_key_value=request.data_format.get("id")
            ).run()

            return None



    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True, isPasswd=True)
    def setOtherMemo(self, request):

        obj = OtherMemo.objects.create(**dict(
            html = request.data_format.get("html"),
            type = request.data_format.get("type")
        ))

        RedisCaCheHandler(
            method="save",
            serialiers="OtherMemoModelSerializerToRedis",
            table="OtherMemo",
            filter_value=obj,
            must_key="id",
        ).run()

        return None