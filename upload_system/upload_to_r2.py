import boto3
import botocore
import os
from tqdm import tqdm

# 配置 Cloudflare R2 端点和凭证
s3_client = boto3.client('s3',
                         endpoint_url='https://a396.r2.cloudflarestorage.com',
                         aws_access_key_id='4e',
                         aws_secret_access_key='9a685c3fabbde1a28a',
                         config=botocore.client.Config(signature_version='s3v4', retries={'max_attempts': 10}))

FOLDER_PATH = r'D:\qbittorrentDownload\anime'
bucket_name = 'anime-web-aliyun'

class ProgressPercentage:
    def __init__(self, filesize):
        self.filesize = filesize
        self._seen_so_far = 0

    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        # Update the overall progress bar
        overall_pbar.update(bytes_amount)

def file_exists_in_r2(bucket_name, object_name):
    """
    检查文件是否已经存在于R2存储桶中
    """
    try:
        s3_client.head_object(Bucket=bucket_name, Key=object_name)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            raise

def upload_folder_to_r2(folder_path, bucket_name):
    files_to_upload = []
    total_size = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            object_name = os.path.relpath(file_path, folder_path).replace("\\", "/")
            if not file_exists_in_r2(bucket_name, object_name):
                files_to_upload.append((file_path, object_name))
                total_size += os.path.getsize(file_path)

    print(f"Total files to upload: {len(files_to_upload)}")

    global overall_pbar
    overall_pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc="Overall Progress", ncols=100, leave=True, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}')
    
    for file_path, object_name in files_to_upload:
        filesize = os.path.getsize(file_path)
        progress = ProgressPercentage(filesize)
        try:
            print(f"\nUploading {object_name}...")
            s3_client.upload_file(file_path, bucket_name, object_name, Callback=progress)
            print(f"Successfully uploaded {object_name}")
        except Exception as e:
            print(f"Error uploading {object_name}: {e}")

    overall_pbar.close()

upload_folder_to_r2(FOLDER_PATH, bucket_name)
