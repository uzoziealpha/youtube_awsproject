import json
import pandas as pd
from googleapiclient.discovery import build
import logging

# Load API credentials from a separate file
def load_credentials():
    with open("config/credentials.json", "r") as f:
        return json.load(f)

# Set up logging
def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

# Fetch video details using YouTube API
def fetch_video_details(youtube_api_key, video_ids):
    youtube = build("youtube", "v3", developerKey=youtube_api_key)
    
    response = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    ).execute()
    
    video_data = []
    for item in response['items']:
        video_data.append({
            "video_id": item["id"],
            "title": item["snippet"]["title"],
            "channel_title": item["snippet"]["channelTitle"],
            "view_count": item["statistics"].get("viewCount", 0),
            "like_count": item["statistics"].get("likeCount", 0),
            "comment_count": item["statistics"].get("commentCount", 0),
            "duration": item["contentDetails"]["duration"],
            "published_at": item["snippet"]["publishedAt"],
            "description": item["snippet"]["description"]
        })
    
    return pd.DataFrame(video_data)

# Main script to test video recommendations
def main():
    credentials = load_credentials()
    setup_logging("logs/youtube_recommendations.log")
    
    try:
        # Load the merged dataset
        user_video_data = pd.read_csv("data/processed/merged_user_video_data.csv")
        
        # Get the list of video IDs from the merged dataset
        video_ids = user_video_data['video_id'].unique()[:5]  # Limit to top 5 for testing
        
        logging.info(f"Fetching details for video IDs: {video_ids}")
        
        # Fetch the video details using YouTube API
        video_details = fetch_video_details(credentials["youtube_api_key"], video_ids)
        
        logging.info(f"Fetched video details successfully.")
        
        # Display the fetched video details
        print(video_details)
        
    except Exception as e:
        logging.error(f"Error occurred while fetching video details: {e}")

if __name__ == "__main__":
    main()
