# pip insatall boto3==1.6.19 required
import os
import sys
from decouple import config
import boto3
from tqdm import tqdm

service_name = 's3'
endpoint_url = 'https://kr.object.ncloudstorage.com'
region_name = 'kr-standard'
access_key = config('NCP_ACCESS_KEY')
secret_key = config('NCP_SECRET_KEY')

# 버킷 목록 조회
def get_bucket_list():
    s3 = boto3.client(
        service_name,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    response = s3.list_buckets()
    for bucket in response.get('Buckets', []):
        print (bucket.get('Name'))
    return 

# 오브젝트 업로드
def upload_object():
    """
    로컬의 images 폴더를 object storage에 업로드
    """
    s3 = boto3.client(
        service_name,
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    bucket_name = config('NCP_BUCKET') # book-thumbnail 버켓
    folder_directory = 'img/' # book-thumbnail/img
    
    # enumerate local files recursively
    local_directory = './project/flask/api/images'
    for root, _, files in os.walk(local_directory):
        for filename in tqdm(files, position=0, leave=True, desc='Uploading..'):
            # construct the full local path
            local_path = os.path.join(root, filename)
            # construct the full Dropbox path
            relative_path = os.path.relpath(local_path, local_directory)
            s3_path = os.path.join(folder_directory, relative_path)
            # print (f'Searching {s3_path} in {bucket_name}')
            try: # 이미 업로드 되어있는지 확인
                s3.head_object(Bucket=bucket_name, Key=s3_path)
                print ("object storage에 %s가 존재합니다. 스킵합니다." % s3_path)
            except: # 버켓에 존재하지 않는 경우 업로드
                s3.upload_file(local_path, bucket_name, s3_path)


if __name__ == '__main__':
    get_bucket_list()
    upload_object()