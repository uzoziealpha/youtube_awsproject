import boto3
import logging
import os
import yaml

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Set up logging
logging.basicConfig(
    filename="logs/upload_to_s3.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Function to upload file to S3
def upload_to_s3(file_path, bucket_name, s3_path):
    s3 = boto3.client('s3')

    if os.path.exists(file_path):
        try:
            s3.upload_file(file_path, bucket_name, s3_path)
            logging.info(f"File {file_path} uploaded to s3://{bucket_name}/{s3_path}")
        except Exception as e:
            logging.error(f"Error uploading file: {e}")
    else:
        logging.error(f"File {file_path} not found!")

if __name__ == "__main__":
    upload_to_s3(
        config["paths"]["processed_data"],
        "your-bucket-name",
        "processed_videos.csv"
    )
