import boto3

s3 = boto3.client('s3')


def download_all_files(bucket_name):
    try:
        list=s3.list_files(Bucket="bucket_name")['Contents']
        for key in list:
            s3.download_files
    except


def main():
    download_all_files()



if __name__ == "__main__":
    main()