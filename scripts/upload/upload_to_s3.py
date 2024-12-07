import boto3

# Configure the AWS S3 client
s3_client = boto3.client('s3')

def upload_file_to_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path  # Use the file name if no object name is provided
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
        print(f"File {file_path} uploaded to {bucket_name}/{object_name}")
    except Exception as e:
        print(f"Error uploading file: {e}")

# Example usage
upload_file_to_s3('data/raw/trending_videos.csv', 'youtube-data-singapore')
