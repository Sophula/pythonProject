import boto3
import botocore


s3_client=boto3.client('s3')

def create_my_bucket(bucket_name):
    try:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f'Bucket '{bucket_name}' was created successfully')
    except botocore.exceptions.ClientError as ex:
        print(ex)

def upload_file_in_bucket(bucket_name, file_path):
    try:
        s3_client.upload_file(file_path, bucket_name, "file.txt")
    except botocore.exceptions.ClientError as ex:
        print(ex)



def main():
    bucket_name="newBucket"
    create_my_bucket(bucket_name)
    upload_file_in_bucket(bucket_name, "test.txt")

if __name__== '__main__':
    main()