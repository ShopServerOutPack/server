
from rest_framework import viewsets
from rest_framework.decorators import list_route

from lib.core.decorator.response import Core_connector

from lib.utils.txcloud import txCloud

class FileAPIView(viewsets.ViewSet):

    @list_route(methods=['POST'])
    @Core_connector()
    def upload(self, request):
        my_file = request.FILES.get('file')

        print(my_file)