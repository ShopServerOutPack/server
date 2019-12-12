
from django.db import models
from lib.utils.mytime import UtilTime

from app.idGenerator import idGenerator

class GoodsCateGory(models.Model):

    """
    商品分类表: 支持无限级扩展
    """

    id = models.AutoField(primary_key=True)

    userid = models.IntegerField(verbose_name="用户代码",null=True)
    gdcgid = models.CharField(max_length=10,default="",verbose_name="分类代码",null=True)
    gdcgname = models.CharField(max_length=120, default="",verbose_name="分类名称",null=True)
    gdcgtitle = models.CharField(max_length=120,default="",verbose_name="标题",null=True,blank=True)
    gdcglastid = models.IntegerField(verbose_name="上级代码",default=0)

    level = models.IntegerField(verbose_name="第几层",default=1)

    sort = models.IntegerField(verbose_name="排序",default=0)

    createtime = models.BigIntegerField(default=0)
    updtime = models.BigIntegerField(default=0)

    istheme = models.CharField(max_length=1, default="1",verbose_name="是否主题,0-是,1-否",null=True)
    isstart = models.CharField(max_length=1, default="1",verbose_name="是否生效,0-是,1-否",null=True)
    url1 = models.CharField(max_length=255, verbose_name="首页封面图", default='', null=True,blank=True)
    url2 = models.CharField(max_length=255, verbose_name="分类封面图", default='', null=True,blank=True)

    islie = models.CharField(max_length=1, verbose_name="是否2列 0-是,1-否", default='1', null=True,blank=True)

    def save(self, *args, **kwargs):

        if not self.gdcgid:
            self.gdcgid = idGenerator.goodscategory()

        t = UtilTime().timestamp
        if not self.createtime:
            self.createtime = t
        self.updtime = t
        return super(GoodsCateGory, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '商品分类表'
        verbose_name_plural = verbose_name
        db_table = 'goodscategory'

class Goods(models.Model):

    """
    商品表
    """

    id = models.AutoField(primary_key=True)

    userid = models.IntegerField(verbose_name="用户代码",null=True)
    gdcgid = models.CharField(max_length=10, verbose_name="分类代码", default="",null=True,blank=True)
    gdcgidtheme = models.CharField(max_length=10, verbose_name="主题分类代码", default="",null=True,blank=True)

    gdid = models.CharField(max_length=10, verbose_name="商品ID", null=True)

    gdname = models.CharField(max_length=120, verbose_name="商品名称", default='', null=True,blank=True)
    gdtitle = models.CharField(max_length=120, verbose_name="商品名称", default='', null=True,blank=True)

    gdtext = models.CharField(max_length=255, verbose_name="描述", default='', null=True,blank=True)
    gdlabel = models.CharField(max_length=255, verbose_name="标签", default='', null=True,blank=True)
    gdimg = models.CharField(max_length=255, verbose_name="封面图", default='', null=True,blank=True)
    gdvideo = models.CharField(max_length=255, verbose_name="视频", default='', null=True,blank=True)

    gdprice = models.DecimalField(max_digits=18,decimal_places=6,default=0.000,verbose_name="商品价格")
    gdnum  = models.IntegerField(verbose_name="商品数量",default=0)
    sort = models.IntegerField(verbose_name="排序",default=0)
    isnew  = models.CharField(max_length=1,verbose_name="是否新品,0-是,1-否",default='1')

    gdsellnum = models.IntegerField(verbose_name="商品售出数量",default=0)

    gdstatus = models.CharField(verbose_name="状态,0-正常,1-下架",default='0',max_length=1)

    gdbrowsenum = models.IntegerField(verbose_name="商品浏览量",default=0)


    createtime = models.BigIntegerField(default=0)
    updtime = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):

        if not self.gdid:
            self.gdid = idGenerator.goods()

        t = UtilTime().timestamp
        if not self.createtime:
            self.createtime = t
        self.updtime = t
        return super(Goods, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '商品表'
        verbose_name_plural = verbose_name
        db_table = 'goods'