import logging
import boto3
from botocore.exceptions import ClientError
from io import StringIO
import yaml

#.github/workflows/main.yaml
with open("/app/main.yaml", "r") as stream:
    try:
        dict = yaml.safe_load(stream)

    except yaml.YAMLError as exc:
        print(exc)

email = (dict["jobs"]["build"]["steps"][1]["with"]["email"])
aws_access_key_id_val = (dict["jobs"]["build"]["steps"][1]["with"]["aws_access_key_id"])
aws_secret_access_key_val = (dict["jobs"]["build"]["steps"][1]["with"]["aws_secret_access_key"])

print(aws_access_key_id_val)
print(aws_secret_access_key_val)



def create_bucket(bucket_name, region="eu-central-1"):

    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    try:
        if region=="eu-central-1":
            s3_client = boto3.client('s3',aws_access_key_id= aws_access_key_id_val,
                        aws_secret_access_key= aws_secret_access_key_val)
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region,aws_access_key_id= aws_access_key_id_val,
                        aws_secret_access_key= aws_secret_access_key_val)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_of_s3_buckets(filename):
    buckets = []
    s3_client = boto3.resource('s3', aws_access_key_id=aws_access_key_id_val,
                             aws_secret_access_key=aws_secret_access_key_val)
    for bucket in s3_client.buckets.all():
        buckets.append(bucket.name)

    return buckets

def dump_file_to_s3(filename):
    s3_client = boto3.resource("s3",aws_access_key_id=aws_access_key_id_val,
                             aws_secret_access_key=aws_secret_access_key_val)
    s3_client.Bucket("stock-time-series").upload_file(Filename=filename,Key=filename)

    print("Data uploaded successfully")

def get_data_from_s3(dataset_name):
    s3_resource = boto3.client('s3', aws_access_key_id=aws_access_key_id_val,
                               aws_secret_access_key=aws_secret_access_key_val)

    obj = s3_resource.get_object(Bucket='stock-time-series', Key=dataset_name)  # 2
    data = obj['Body'].read().decode('utf-8')
    data = StringIO(data)
    return data
