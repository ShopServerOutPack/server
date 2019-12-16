
import os

from rest_framework import viewsets
from lib.core.decorator.response import Core_connector
from project.settings import IMAGE_PATH
from project.config_include.common import ServerUrl
from lib.utils.mytime import UtilTime
from lib.utils.exceptions import PubErrorCustom
from rest_framework.decorators import list_route

class FileAPIView(viewsets.ViewSet):

    @list_route(methods=['POST','OPTIONS'])
    @Core_connector()
    def upload(self,request, *args, **kwargs):

        file_obj = request.FILES.get('file')
        img_type = file_obj.name.split('.')[1]
        img_type = img_type.lower()

        if img_type in ['png', 'jpg', 'jpeg', 'gif']:
            timestr = UtilTime().arrow_to_string(format_v="YYYYMMDD")
            path = os.path.join(IMAGE_PATH, '{}'.format(timestr))

            if os.path.exists(os.path.join(path,file_obj.name)):
                c=0
                while True:
                    if len(file_obj.name.split('images_teshudaima_images'))>1:
                        file_obj.name = file_obj.name.split('images_teshudaima_images')[1]
                    file_obj.name="copy{}images_teshudaima_images{}".format(c,file_obj.name)
                    c=c+1
                    if not os.path.exists(os.path.join(path,file_obj.name.replace("images_teshudaima_images","_"))):
                        file_obj.name = file_obj.name.replace("images_teshudaima_images","_")
                        break
            if not os.path.exists(path):
                os.makedirs(path)

            with open(os.path.join(path,file_obj.name),'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            return {"data":{
                "path":"{}/statics/images/{}/{}".format(ServerUrl,timestr,file_obj.name),
                "name":file_obj.name
            }}
        else:
            raise PubErrorCustom("文件类型有误!")

        return None