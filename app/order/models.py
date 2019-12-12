
from django.db import models
from lib.utils.mytime import UtilTime

from app.idGenerator import idGenerator

class ShopCart(models.Model):

    """
    购物车表
    """

    id = models.BigAutoField(primary_key=True,verbose_name="ID")

    userid = models.BigIntegerField(verbose_name="用户代码",null=True)
    gdid = models.CharField(max_length=10, verbose_name="商品ID", null=True)
    gdimg = models.CharField(max_length=255, verbose_name="封面图", default='', null=True, blank=True)
    gdname = models.CharField(max_length=120, verbose_name="商品名称", default='', null=True, blank=True)
    gdprice = models.DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="商品价格")
    gdnum  = models.IntegerField(verbose_name="商品数量",default=0)

    createtime = models.BigIntegerField(default=0)
    updtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):

        t = UtilTime().timestamp
        if not self.createtime:
            self.createtime = t
        self.updtime = t
        return super(ShopCart, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '购物车表'
        verbose_name_plural = verbose_name
        db_table = 'shopcart'

class OrderGoodsLink(models.Model):

    """
    订单商品关联表
    """

    linkid = models.BigAutoField(primary_key=True,verbose_name="ID")
    userid = models.BigIntegerField(verbose_name="用户代码",null=True)
    orderid = models.CharField(max_length=19,verbose_name="订单ID",null=True,default="")
    gdid = models.CharField(max_length=10, verbose_name="商品ID", null=True)
    gdimg = models.CharField(max_length=255, verbose_name="封面图", default='', null=True, blank=True)
    gdname = models.CharField(max_length=120, verbose_name="商品名称", default='', null=True, blank=True)
    gdprice = models.DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="商品价格")
    gdnum  = models.IntegerField(verbose_name="商品数量",default=0)

    createtime = models.BigIntegerField(default=0)
    updtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):

        t = UtilTime().timestamp
        if not self.createtime:
            self.createtime = t
        self.updtime = t
        return super(OrderGoodsLink, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '订单商品关联表'
        verbose_name_plural = verbose_name
        db_table = 'ordergoodslink'


class Order(models.Model):

    """
    订单表
    """

    id = models.BigAutoField(primary_key=True,verbose_name="ID")

    orderid = models.CharField(max_length=19,verbose_name="订单ID",null=True)
    linkid = models.CharField(max_length=255,verbose_name="关联表集合",default="")

    userid = models.BigIntegerField(verbose_name="用户代码", null=True)

    amount = models.DecimalField(verbose_name="交易金额",max_digits=18,decimal_places=6,default=0.0)
    payamount = models.DecimalField(verbose_name="实际支付金额",max_digits=18,decimal_places=6,default=0.0)

    status = models.CharField(max_length=1,verbose_name="状态,0-待付款,1-已付款",default="0")

    createtime = models.BigIntegerField(default=0)
    updtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):

        if not self.orderid:
            self.orderid = idGenerator.ordercode()

        t = UtilTime().timestamp
        if not self.createtime:
            self.createtime = t
        self.updtime = t
        return super(Order, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '订单表'
        verbose_name_plural = verbose_name
        db_table = 'order'