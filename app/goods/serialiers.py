
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from app.goods.models import GoodsCateGory,Goods,GoodsTheme,Card,Cardvirtual
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