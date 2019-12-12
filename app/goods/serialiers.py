
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from app.goods.models import GoodsCateGory,Goods

class GoodsCateGoryModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = GoodsCateGory
        fields = '__all__'

        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=GoodsCateGory.objects.all(),
        #         fields=('gdcgid',),
        #         message="登录名重复！"
        #     ),
        # ]
class GoodsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'