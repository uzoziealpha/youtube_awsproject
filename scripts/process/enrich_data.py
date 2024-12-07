import io
import pandas as pd
import boto3

# Function to upload a DataFrame to S3
def upload_to_s3(df, bucket_name, file_key):
    csv_buffer = io.StringIO()  # Creates an in-memory text stream
    df.to_csv(csv_buffer, index=False)  # Writes the DataFrame to the buffer
    csv_buffer.seek(0)  # Moves the buffer position to the start of the data
    s3 = boto3.client('s3')  # Create an S3 client
    s3.put_object(Bucket=bucket_name, Body=csv_buffer.getvalue(), Key=file_key)  # Uploads to S3
