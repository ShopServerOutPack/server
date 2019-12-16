
import json
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from lib.utils.exceptions import PubErrorCustom

from app.cache.utils import RedisCaCheHandler
from app.order.models import Order,OrderGoodsLink

from app.order.serialiers import OrderModelSerializer,AddressModelSerializer
from app.order.models import Address

class OrderAPIView(viewsets.ViewSet):


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def addAddress(self, request):

        data = request.data_format.get('data',None)
        if str(data.get('moren')) == '0':
            Address.objects.filter(userid=request.user['userid']).update(moren='1')

        if 'id' in data:
            try:
                address = Address.objects.select_for_update().get(id=data['id'])
            except Address.DoesNotExist:
                raise PubErrorCustom("该地址不存在!")

            address.name = data.get("name")
            address.phone = data.get("phone")
            address.detail = data.get("detail")
            address.label = data.get("label")
            address.moren = data.get("moren")
            address.save()
        else:
            address = Address.objects.create(**dict(
                userid=request.user['userid'],
                name = data.get("name"),
                phone = data.get("phone"),
                detail = data.get("detail"),
                label = data.get("label"),
                moren = data.get("moren"),
            ))

        return {"data":AddressModelSerializer(address,many=False).data}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def delAddress(self, request):

        Address.objects.filter(id=request.data_format['id']).delete()



    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def OrderPays(self, request):

        if not len(request.data_format['shopcart']):
            raise PubErrorCustom("购买商品不能为空!")

        orderObj = Order.objects.create(**dict(
            userid=request.user['userid']
        ))
        orderObj.linkid={"linkids":[]}
        orderObj.amount = 0.0


        for item in request.data_format['shopcart']:
            res = RedisCaCheHandler(
                method="get",
                table="goods",
                must_key_value=item['gdid'],
            ).run()
            if not res:
                raise PubErrorCustom("{}商品已下架,请在购物车删除此商品!".format(item['gdname']))

            link = OrderGoodsLink.objects.create(**dict(
                userid = request.user['userid'],
                orderid = orderObj.orderid,
                gdid = res['gdid'],
                gdimg = res['gdimg'],
                gdname = res['gdname'],
                gdprice = res['gdprice'],
                gdnum = item['gdnum']
            ))

            orderObj.linkid['linkids'].append(link.linkid)
            orderObj.amount += float(link.gdprice) * link.gdnum
        orderObj.linkid=json.dumps(orderObj.linkid)
        orderObj.save()
        return None

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def OrderPaysByOrder(self, request):

        if not request.data_format.get('orderid',None):
            raise PubErrorCustom("订单号为空!")

        try:
            order = Order.objects.select_for_update().get(orderid=request.data_format.get('orderid',None))
        except Order.DoesNotExist:
            raise PubErrorCustom("订单异常!")

        order.status='1'
        order.save()

        return None

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def OrderGet(self, request):

        orderQuery = Order.objects.filter(userid=request.user['userid'])

        if request.query_params_format.get("status"):
            orderQuery = orderQuery.filter(status=request.query_params_format.get("status"))


        print(request.query_params_format.get("page"))
        page=int(request.query_params_format.get("page"))

        page_size = 10 if not request.query_params_format.get("page_size",None) else request.query_params_format.get("page_size",None)
        page_start = page_size * page  - page_size
        page_end = page_size * page

        return {
            "data":OrderModelSerializer(orderQuery.order_by('-createtime')[page_start:page_end],many=True).data
        }
