import boto3

# 配置 Cloudflare R2 端点和凭证
s3_client = boto3.client('s3',
                         endpoint_url='https://ae7b21228c0af396feb1372330a8b87a.r2.cloudflarestorage.com',
                         aws_access_key_id='4ebfc38641a6ea825bdbdf141d67b2f8',
                         aws_secret_access_key='9a685c3fabb3a75d4894a6ecadf074afb9729d3bb3cba86646de1a28a3f5bea7')

# 列出指定存储桶中的对象
bucket_name = 'anime-web-aliyun'

try:
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    print(f'Objects in bucket {bucket_name}:')
    for obj in response.get('Contents', []):
        print(f'- {obj["Key"]}')
except Exception as e:
    print(f'Error: {e}')