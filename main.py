import boto3
from os import getenv

AWS_ACCESS_KEY = getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = getenv("AWS_SECRET_KEY")

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)
s3 = boto3.client('s3')

def main():
    response = s3.list_buckets()

    print('All S3 buckets:')
    for bucket in response['Buckets']:
        print(f' {bucket["Name"]}')

#        if bucket.startswith('prod'):
#           print(f' {bucket["Name"]}')

if __name__ == "__main__":
    main()
