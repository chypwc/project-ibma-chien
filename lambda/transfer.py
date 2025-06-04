import boto3
import os
import tempfile
import pandas as pd

s3 = boto3.client('s3')
DEST_BUCKET = os.environ['DEST_BUCKET']

def lambda_handler(event, context):
    for record in event['Records']:
        src_bucket = record['s3']['bucket']['name']
        src_key = record['s3']['object']['key']

        print(f"Processing file: {src_key} from {src_bucket}")

        if src_key.lower().endswith('.csv'):
            with tempfile.TemporaryDirectory() as tmpdir:
                csv_path = os.path.join(tmpdir, 'file.csv')
                parquet_path = os.path.join(tmpdir, 'file.parquet')

                # Download the CSV
                s3.download_file(src_bucket, src_key, csv_path)

                # Convert to Parquet
                df = pd.read_csv(csv_path)
                df.to_parquet(parquet_path, index=False)

                # Define new key name
                dst_key = src_key.rsplit('.', 1)[0] + '.parquet'

                # Upload Parquet file
                s3.upload_file(parquet_path, DEST_BUCKET, dst_key)
                print(f"Converted and uploaded {dst_key} to {DEST_BUCKET}")

        else:
            # If not CSV, just copy as-is
            copy_source = {'Bucket': src_bucket, 'Key': src_key}
            s3.copy_object(Bucket=DEST_BUCKET, CopySource=copy_source, Key=src_key)
            print(f"Copied {src_key} to {DEST_BUCKET}")