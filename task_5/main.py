import boto3
from pathlib import Path
from botocore.exceptions import ClientError
import time

s3 = boto3.client('s3')
client = boto3.client('lambda')

iam = boto3.client('iam')
file_extensions = ['.jpg', '.jpeg', '.png']


def create_my_bucket(bucket):
    try:
        s3.create_bucket(Bucket=bucket)
    except Exception as ex:
        print(ex)

def add_permission_to_my_bucket(function, bucket):
    client.add_permission(
        FunctionName=function,
        StatementId='1',
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=f'arn:aws:s3:::{bucket}',
    )

def convert_to_bytes(zip):
    with open(zip, 'rb') as file_data:
        bytes_content = file_data.read()
    return bytes_content


def create_my_function(function, role, zip):
    try:
        client.create_function(
            FunctionName=function,
            Runtime='python3.8',
            Role=iam.get_role(RoleName=role)['Role']['Arn'],
            Handler='lambda_function.lambda_handler',
            Code={
                'ZipFile': convert_to_bytes(zip)
            },
        )
        print(f'Function with name {function} was created successfully')

    except Exception as ex:
        print(ex)



def trigger_of_s3(bucket, function):
    lambda_foreach = []
    for extension in file_extensions:
        lambda_foreach.append({
            'LambdaFunctionArn': client.get_function(
                FunctionName=function)['Configuration']['FunctionArn'],
            'Events': [
                's3:ObjectCreated:*'
            ],
            'Filter': {
                'Key': {
                    'FilterRules': [
                        {
                            'Name': 'suffix',
                            'Value': extension
                        },
                    ]
                }
            }
        },)
    try:
        add_permission_to_my_bucket(fuction, bucket)
        s3.put_bucket_notification_configuration(
            Bucket=bucket,
            NotificationConfiguration={
                'LambdaFunctionConfigurations': lambda_foreach,
            }
        )
        print(f'Following function {function} was successfully added to {bucket}')

    except Exception as ex:
        print(ex)

def upload_my_file(file, bucket):
    s3.upload_file(file, bucket)


def read_my_file(bucket, file):
    try:
        time.sleep(70)
        data = s3.get_object(Bucket=bucket, Key=file.replace('.jpg', '.json'))
        contents = data['Body'].read()
        print(contents)

    except Exception as ex:
        print(ex)


def main(file, bucket, role, function, zip):

    create_my_bucket(bucket)
    create_my_function(function, role, zip)

    trigger_of_s3(bucket, function)
    upload_my_file(file, bucket)
    read_my_file(bucket, file)

if __name__ == '__main__':
    main('meme.jpg', 'meme_bucket', 'LabRole', 'my-lambda-function', './lambda_function.zip')