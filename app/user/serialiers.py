
import json
from rest_framework import serializers
from app.user.models import Users

class UsersSerializers(serializers.Serializer):

    userid = serializers.IntegerField()
    pic = serializers.CharField()
    name = serializers.CharField()
