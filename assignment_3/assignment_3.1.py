import boto3
import argparse

s3 = boto3.client('s3')

def upload_file(file_name, bucket_name, object_name=None):
    try:
        with open(file_name, "rb") as file:
            s3.upload_fileobj(file, bucket_name, object_name)
            print('File was successfully uploaded in bucket')
    except Exception as ex:
        print(ex)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bucket_name')
    parser.add_argument('-f', '--file_name')
    parsed = parser.parse_args()
    upload_file(parsed.file_name, parsed.bucket_name)


if __name__ == '__main__':
    main()