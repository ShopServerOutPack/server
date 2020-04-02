
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from app.goods.models import GoodsCateGory,Goods,GoodsTheme,Card,Cardvirtual,DeliveryCode
from lib.utils.mytime import UtilTime

class GoodsCateGoryModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = GoodsCateGory
        fields = '__all__'

class GoodsThemeModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = GoodsTheme
        fields = '__all__'

class GoodsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'

class GoodsForSearchSerializer(serializers.Serializer):

    gdid = serializers.CharField()
    gdname = serializers.CharField()
    gdprice = serializers.DecimalField(max_digits=16,decimal_places=2)
    gdimg = serializers.CharField()
    gdtext = serializers.CharField()


class CardModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'

class CardvirtualModelSerializer(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()
    status_format = serializers.SerializerMethodField()

    def get_status_format(self,obj):
        return '是' if obj.status == '0' else '否'

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = Cardvirtual
        fields = '__all__'


class DeliveryCodeModelSerializer(serializers.ModelSerializer):

    createtime_format = serializers.SerializerMethodField()
    status_format = serializers.SerializerMethodField()

    def get_status_format(self,obj):
        return '是' if obj.status == '0' else '否'

    def get_createtime_format(self,obj):
        return UtilTime().timestamp_to_string(obj.createtime)

    class Meta:
        model = DeliveryCode
        fields = '__all__'