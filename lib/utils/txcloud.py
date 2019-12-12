

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client




from sts.sts import Sts

class txCloud(object):
    def __init__(self):
        secret_id = 'AKID0mJacYZuGLAKSLP01i7GAoHfpkPsvED6'  # 替换为用户的 secretId
        secret_key = 'B7mBLFtIeokUJvNcfWVK1c0EzgAIC7nD'  # 替换为用户的 secretKey
        region = 'ap-shanghai'  # 替换为用户的 Region
        token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
        scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
        config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
        self.client = CosS3Client(config)

    def run(self):
        config = {
            # 临时密钥有效时长，单位是秒
            'duration_seconds': 1800,
            # 固定密钥
            'secret_id': 'AKID0mJacYZuGLAKSLP01i7GAoHfpkPsvED6',
            # 固定密钥
            'secret_key': 'B7mBLFtIeokUJvNcfWVK1c0EzgAIC7nD',
            # 是否需要设置代理
            # 'proxy': {
            #   'http': 'XXX',
            #   'https': 'XXX'
            # },
            # 换成你的 bucket
            'bucket': 'yijingxisui-1254541031',
            # 换成 bucket 所在地区
            'region': 'ap-shanghai',
            # 这里改成允许的路径前缀，可以根据自己网站的用户登录态判断允许上传的具体路径
            # 例子： a.jpg 或者 a/* 或者 * (使用通配符*存在重大安全风险, 请谨慎评估使用)
            'allow_prefix': '*',
            # 密钥的权限列表。简单上传和分片需要以下的权限，其他权限列表请看 https://cloud.tencent.com/document/product/436/31923
            'allow_actions': [
                # 简单上传
                'name/cos:PutObject',
                # 表单上传
                'name/cos:PostObject',
                # 分片上传： 初始化分片
                'name/cos:InitiateMultipartUpload',
                # 分片上传： 查询 bucket 中未完成分片上传的UploadId
                "name/cos:ListMultipartUploads",
                # 分片上传： 查询已上传的分片
                "name/cos:ListParts",
                # 分片上传： 上传分片块
                "name/cos:UploadPart",
                # 分片上传： 完成分片上传
                "name/cos:CompleteMultipartUpload"
            ]

        }
        sts = Sts(config)
        response = sts.get_credential()
        return response

    # def putObject(self,filepath,filename):
    #     with open("{}{}".format(filepath,filename), 'rb') as fp:
    #         response = self.client.put_object(
    #             Bucket='yijingxisui-1254541031',
    #             Body=fp,
    #             Key=filename,
    #             StorageClass='STANDARD',
    #             EnableMD5=True
    #         )
    #     print(response['ETag'])