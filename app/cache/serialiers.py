
from rest_framework import serializers

from lib.utils.mytime import UtilTime
from lib.utils.exceptions import PubErrorCustom
from app.user.models import Users,Role
from app.public.models import Banner,AttachMentGroup,AttachMent,OtherMemo
from app.goods.models import GoodsCateGory,Goods,GoodsTheme,Card

class UserModelSerializerToRedis(serializers.ModelSerializer):

    role = serializers.SerializerMethodField()
    createtime_format = serializers.SerializerMethodField()
    bal = serializers.SerializerMethodField()

    isvip_format = serializers.SerializerMethodField()

    def get_role(self,obj):
        try:
            roleObj = Role.objects.get(rolecode=obj.rolecode)
            return RoleModelSerializerToRedis(roleObj,many=False).data
        except Role.DoesNotExist:
            raise PubErrorCustom("无此角色信息!")

    def get_isvip_format(self,obj):
        if str(obj.isvip) == "1":
            return "是"
        else:
            return "否"

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    def get_bal(self,obj):
        return round(float(obj.bal),2)

    class Meta:
        model = Users
        fields = '__all__'

class RoleModelSerializerToRedis(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'

class BannerModelSerializerToRedis(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = '__all__'

class GoodsCateGoryModelSerializerToRedis(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()
    status_format = serializers.SerializerMethodField()

    def get_status_format(self,obj):
        return '是' if obj.status == '0' else '否'

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = GoodsCateGory
        fields = '__all__'

class GoodsThemeModelSerializerToRedis(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()
    status_format = serializers.SerializerMethodField()

    def get_status_format(self,obj):
        return '是' if obj.status == '0' else '否'

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = GoodsTheme
        fields = '__all__'


class GoodsModelSerializerToRedis(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()

    gdprice = serializers.DecimalField(max_digits=16,decimal_places=2)

    gdstatus_format = serializers.SerializerMethodField()

    def get_gdstatus_format(self,obj):
        return '是' if obj.gdstatus == '0' else '否'

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = Goods
        fields = '__all__'


class CardModelSerializerToRedis(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()

    # username = serializers.SerializerMethodField()
    bal = serializers.DecimalField(max_digits=18,decimal_places=2)

    # def get_username(self,obj):
    #     return Users.objects.get(userid=obj.useuserid).name if obj.useuserid>0 else ""

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = Card
        fields = '__all__'


class AttachMentGroupModelSerializerToRedis(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = AttachMentGroup
        fields = '__all__'

class AttachMentModelSerializerToRedis(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = AttachMent
        fields = '__all__'

class OtherMemoModelSerializerToRedis(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = OtherMemo
        fields = '__all__'