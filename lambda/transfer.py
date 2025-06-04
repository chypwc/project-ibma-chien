import boto3
import os

s3 = boto3.client('s3')
DEST_BUCKET = os.environ['DEST_BUCKET']

def lambda_handler(event, context):
    for record in event['Records']:
        src_bucket = record['s3']['bucket']['name']
        src_key = record['s3']['object']['key']
        copy_source = {'Bucket': src_bucket, 'Key': src_key}
        print(f"Copying {src_key} from {src_bucket} to {DEST_BUCKET}")
        s3.copy_object(Bucket=DEST_BUCKET, CopySource=copy_source, Key=src_key)