
import json
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector
from lib.utils.exceptions import PubErrorCustom

from app.cache.utils import RedisCaCheHandler
from app.order.models import Order,OrderGoodsLink

from app.order.serialiers import OrderModelSerializer

class OrderAPIView(viewsets.ViewSet):

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isWechatTicket=True)
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

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isWechatTicket=True)
    def OrderGet(self, request):

        orderQuery = Order.objects.filter(status=str(request.query_params_format.get("status")),userid=request.user['userid'])

        page_size=10
        print(request.query_params_format.get("page"))
        page=int(request.query_params_format.get("page"))
        page_start = page_size * page  - page_size
        page_end = page_size * page

        return {
            "data":OrderModelSerializer(orderQuery.order_by('-createtime')[page_start:page_end],many=True).data
        }
