
import json
from rest_framework import viewsets
from rest_framework.decorators import list_route

from django.db import transaction
from django.http import HttpResponse
from lib.core.decorator.response import Core_connector
from lib.utils.exceptions import PubErrorCustom

from app.cache.utils import RedisCaCheHandler
from app.order.models import Order,OrderGoodsLink

from app.user.models import Users

from app.order.serialiers import OrderModelSerializer,AddressModelSerializer
from app.order.models import Address

from app.goods.models import Card

from app.order.utils import wechatPay

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
    def OrderCreate(self, request):
        """
        生成订单
        :param request:
        :return:
        """

        if not len(request.data_format['shopcart']):
            raise PubErrorCustom("购买商品不能为空!")

        orderObj = Order.objects.create(**dict(
            userid=request.user['userid']
        ))
        orderObj.linkid={"linkids":[]}
        orderObj.amount = 0.0

        for item in request.data_format['shopcart']:
            if not item['selected']:
                continue

            res = RedisCaCheHandler(
                method="get",
                table="goods",
                must_key_value=item['gdid'],
            ).run()
            if not res or res['gdstatus']=='1':
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

        return {"data":orderObj.orderid}


    # @list_route(methods=['POST'])
    # @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    # def PayOrderPre(self,request):
    #     """
    #     预支付
    #     :param request:
    #     :return:
    #     """
    #     if not request.data_format.get('orderid',None):
    #         raise PubErrorCustom("订单号为空!")
    #
    #     try:
    #         user = Users.objects.get(userid=request.user.get("userid"))
    #     except Users.DoesNotExist:
    #         raise PubErrorCustom("用户不存在!")
    #
    #     try:
    #         order = Order.objects.select_for_update().get(orderid=request.data_format.get('orderid',None))
    #         order.address = json.dumps(request.data_format.get('address',{}))
    #         if order.status=='1':
    #             raise PubErrorCustom("此点单已付款!")
    #     except Order.DoesNotExist:
    #         raise PubErrorCustom("订单异常!")


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def OrderPaysByOrder(self, request):

        if not request.data_format.get('orderid',None):
            raise PubErrorCustom("订单号为空!")

        try:
            user = Users.objects.select_for_update().get(userid=request.user.get("userid"))
        except Users.DoesNotExist:
            raise PubErrorCustom("用户不存在!")

        try:
            order = Order.objects.select_for_update().get(orderid=request.data_format.get('orderid',None))
            order.address = json.dumps(request.data_format.get('address',{}))
            if order.status=='1':
                raise PubErrorCustom("此点单已付款!")
        except Order.DoesNotExist:
            raise PubErrorCustom("订单异常!")

        amount = float(order.amount)

        print(request.data_format.get('usebal'))
        if request.data_format.get('usebal'):
            if float(user.bal) >= amount:
                user.bal = float(user.bal) - amount
                order.balamount = amount
                order.status = '1'
                user.save()
                order.save()
                return {"data":{"usebalall":True}}
            else:
                amount -= float(user.bal)
                order.balamount = user.bal
                order.payamount = amount
                order.save()
        print(amount)
        #request.META.get("HTTP_X_REAL_IP"),
        data = wechatPay().request({
            "out_trade_no" : order.orderid,
            "total_fee" : int(amount * 100),
            "spbill_create_ip" : "192.168.0.1",
            "openid": user.uuid
        })

        return {"data":data}

    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def txPayOrderQuery(self, request):

        return wechatPay().orderQuery(request.data_format['orderid'])

    @list_route(methods=['POST','GET'])
    def txPayCallback(self, request):
        try:
            with transaction.atomic():
                wechatPay().callback(request)
            return HttpResponse("""<xml><return_code><![CDATA[SUCCESS]]></return_code>
                                <return_msg><![CDATA[OK]]></return_msg></xml>""",
                            content_type='text/xml', status=200)
        except Exception:
            return HttpResponse("""<xml><return_code><![CDATA[FAIL]]></return_code>                          
                                    <return_msg><![CDATA[Signature_Error]]></return_msg></xml>""",
                                         content_type = 'text/xml', status = 200)


    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def OrderGet(self, request):

        orderQuery = Order.objects.filter(userid=request.user['userid'])

        if request.query_params_format.get("status"):
            orderQuery = orderQuery.filter(status=request.query_params_format.get("status"))

        if request.query_params_format.get("orderid"):
            orderQuery = orderQuery.filter(orderid=request.query_params_format.get("orderid"))

        page=int(request.query_params_format.get("page",1))

        page_size = request.query_params_format.get("page_size",10)
        page_start = page_size * page  - page_size
        page_end = page_size * page

        try:
            user = Users.objects.get(userid=request.user.get("userid"))
        except Users.DoesNotExist:
            raise PubErrorCustom("用户不存在!")

        return {
            "data":{
                "order":OrderModelSerializer(orderQuery.order_by('-createtime')[page_start:page_end],many=True).data,
                "bal": "%.2lf"%user.bal
            }
        }

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True)
    def OrderByOrderidQuery(self, request):
        try:
            orderQuery = Order.objects.get(orderid=request.query_params_format.get("orderid"))
        except Order.DoseNotExists:
            raise PubErrorCustom("订单号不存在!")

        try:
            user = Users.objects.get(userid=request.user.get("userid"))
        except Users.DoesNotExist:
            raise PubErrorCustom("用户不存在!")

        return {
            "data": {
                "order":OrderModelSerializer(orderQuery, many=False).data,
                "bal" : "%.2lf"%user.bal
            }
        }

    @list_route(methods=['GET'])
    @Core_connector(isPasswd=True,isTicket=True,isPagination=True)
    def queryOrderAll(self,request):

        queryClass = Order.objects.filter()

        return {"data":OrderModelSerializer(queryClass.order_by('-createtime'),many=True).data}


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def cardCz(self,request):

        print(request.data_format)
        account = request.data_format['account']
        password = request.data_format['password']

        try:
            card = Card.objects.select_for_update().get(account=account,password=password,type='0')
            if card.useuserid>0:
                return {"data": False}
        except Card.DoesNotExist:
            return {"data":False}
        try:
            user = Users.objects.select_for_update().get(userid=request.user['userid'])
        except Users.DoesNotExist:
            raise PubErrorCustom("用户非法!")


        user.bal = float(user.bal+card.bal)
        user.save()

        card.useuserid = user.userid
        card.save()

        RedisCaCheHandler(
            method="save",
            serialiers="CardModelSerializerToRedis",
            table="card",
            filter_value=card,
            must_key="id",
        ).run()

        return {"data":True}


    @list_route(methods=['POST'])
    @Core_connector(isTransaction=True,isPasswd=True,isTicket=True)
    def orderFh(self,request):
        print(request.data_format.get("orders"))
        orders = Order.objects.filter(orderid__in=request.data_format.get("orders"))
        for item in orders:
            item.fhstatus = '0'
            item.save()

        return None


