import argparse
from os import getenv
import boto3
from boto3 import s3
from botocore.config import Config

AWS_REGION = getenv("AWS_REGION", "eu-central-1")

custom_config = Config(region_name=AWS_REGION)
s3_client = boto3.client("s3", config=custom_config)


def print_bucket_with_name(bucket_name):
    response = s3.list_buckets()
    bucket_exists = False

    for buck in response['Buckets']:
        if buck["Name"] == bucket_name:
            bucket_exists = True
            print(f"Bucket called {bucket_name} already exists")

    if not bucket_exists == True:
            create_bucket_with_name(bucket_name)

def create_bucket_with_name(bucket_name):
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} has been created")
    except Exception as ex:
        print(ex)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name')
    parsed = parser.parse_args()
    print_bucket_with_name(parsed.name)

if __name__ == "__main__":
    main()