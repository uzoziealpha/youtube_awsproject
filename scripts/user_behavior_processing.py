import pandas as pd
import boto3
import io
import sys

# Ensuring default encoding (not necessary in most cases but added for clarity)
# sys.setdefaultencoding('utf-8')  # Not needed in Python 3

# Function to load user behavior data from a CSV file or S3 bucket
def load_user_data(file_path='data/raw/user_behavior.csv'):
    try:
        # Open with explicit UTF-8 encoding to avoid potential issues
        user_data = pd.read_csv(file_path, encoding='utf-8')
        print("User data loaded successfully.")
        return user_data
    except Exception as e:
        print(f"Error loading user data: {e}")
        return None

# Function to load video metadata from an S3 bucket
def load_video_metadata_from_s3(bucket_name='youtube-data-singapore', file_key='data/raw/trending_videos.csv'):
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        # Ensure we're reading the file with UTF-8 encoding
        video_data = pd.read_csv(io.BytesIO(obj['Body'].read()), encoding='utf-8')
        print("Video metadata loaded successfully.")
        return video_data
    except Exception as e:
        print(f"Error loading video metadata from S3: {e}")
        return None

# Function to merge user data with video metadata
def merge_user_video_data(user_data, video_data):
    merged_data = pd.merge(user_data, video_data, on='video_id', how='inner')
    print("User and video data merged successfully.")
    return merged_data

# Main function
if __name__ == "__main__":
    # Load the data
    user_data = load_user_data()
    video_data = load_video_metadata_from_s3()

    # Check if data was loaded successfully before merging
    if user_data is not None and video_data is not None:
        combined_data = merge_user_video_data(user_data, video_data)
        # Optionally save the combined data to a CSV for review or use in further processing
        combined_data.to_csv('data/processed/merged_user_video_data.csv', index=False, encoding='utf-8')
        print("Combined data saved to 'data/processed/merged_user_video_data.csv'.")
