import boto3

# 配置 Cloudflare R2 端点和凭证
s3_client = boto3.client('s3',
                         endpoint_url='https://a.r2.cloudflarestorage.com',
                         aws_access_key_id='4eb',
                         aws_secret_access_key='9a687')

# 列出指定存储桶中的对象
bucket_name = 'anime-web-aliyun'

try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    print(f'Objects in bucket {bucket_name}:')
    for obj in response.get('Contents', []):
        print(f'- {obj["Key"]}')
except Exception as e:
    print(f'Error: {e}')
